import logging
from multiprocessing import Pool, cpu_count

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

logger = logging.getLogger("cassa-distance-matrix")


def compute_earth_mover_dist(first, second):
    """
    Compute earth's mover distance (EMD) between two data tensors.

    Parameters
    ----------
    first : np.ndarray
        First data array
    second : np.ndarray
        Second data array

    Returns
    ----------
    emd_val : float
        EMD distance between the two arrays
    """
    d = cdist(first, second)
    assignment = linear_sum_assignment(d)
    emd_val = d[assignment].sum()
    return emd_val


class DistanceMatrix(object):
    """
    Distance matrix class

    This class allows computation of distance matrix.
    """

    def __init__(self, data_tensor):
        """
        Parameters
        ----------
        data_tensor : np.ndarray
            3-D data tensor
        """
        self.data = data_tensor

        self.n = self.data.shape[0]

        # Get indices for the upper-triangle of matrix array
        self.indx, self.indy = np.triu_indices(self.n)

        self.k_max = len(self.indx)  # maximum elements in 1D dist array
        self.k_step = self.n ** 2 // 500  # ~500 bulks
        self.k_step_new_data = int(self.n / 5)

    def _emd_proc(self, start):
        """
        Process for EMD computation.

        Parameters
        ----------
        start : int
        """
        dist = []
        k1 = start
        k2 = min(start + self.k_step, self.k_max)
        for k in range(k1, k2):
            # get (i, j) for 2D distance matrix knowing (k) for 1D distance matrix
            i = self.indx[k]
            j = self.indy[k]
            # store distance
            a = self.data[i, :, :]
            b = self.data[j, :, :]
            d = compute_earth_mover_dist(a, b)
            dist.append(d)
        return k1, k2, dist

    def _emd_proc_new_data(self, start):
        """
        Process for EMD computation for new data.

        Parameters
        ----------
        start : int
        """
        dist = []
        k1 = start
        k2 = min(start + self.k_step_new_data, self.n)
        for k in range(k1, k2):
            # store distance
            a = self.data[k, :, :]
            b = self.new_data
            d = compute_earth_mover_dist(a, b)
            dist.append(d)
        return k1, k2, dist

    def _compute_distance_matrix_parallel(self, metric="emd", n_proc=cpu_count()):
        """
        Compute EMD distance matrix in parallel.

        Parameters
        ----------
        metric : str, optional
            Metric to be used. Defaults to EMD.
        n_proc : int, optional
            Number of processes. Defaults to cpu_count().

        """
        if metric == "emd":
            dist_proc = self._emd_proc
        else:
            logger.error(" Only EMD metric implemented.")
            raise ValueError

        try:
            from progress.bar import Bar

            progress_module = True

        except ImportError:
            progress_module = False

        # 2-D matrix to fill with distances
        np_arr = np.zeros((self.n, self.n))
        # resulting 1D dist array
        dist = np.zeros(self.k_max)

        if progress_module:
            bar = Bar(
                "Calculating distance matrix... ", max=len(self.indx) / self.k_step
            )

        with Pool(n_proc) as pool:
            for k1, k2, res in pool.imap_unordered(
                dist_proc, range(0, self.k_max, self.k_step)
            ):
                dist[k1:k2] = res

                if progress_module:
                    bar.next()
                else:
                    continue

        if progress_module:
            bar.finish()

        np_arr[self.indx, self.indy] = dist
        # Construct lower-triangle (it is a symmetric matrix)
        i_lower = np.tril_indices(len(self.data), -1)
        np_arr[i_lower] = np_arr.T[i_lower]
        logger.info(" Constructed entire distance matrix")
        return np_arr

    def _compute_distance_matrix_serial(self, metric="emd"):
        """Compute distance matrix.

        Parameters
        ----------
        matrix_arrays : np.ndarray
            Matrix of data tensors stored in arrays.
            Only 1-D or 2-D data tensors allowed

        """
        if metric != "emd":
            logger.error(" Only EMD metric implemented.")
            raise ValueError

        # 2-D matrix to fill with distances
        np_arr = np.zeros((self.n, self.n))

        if len(self.data.shape) == 2:
            # for a matrix of 1-D data tensors
            arr_1 = self.data[self.indx][:, np.newaxis]
            arr_2 = self.data[self.indy][:, np.newaxis]

        elif len(self.data.shape) == 3:
            # for a matrix of 2-D data tensors
            arr_1 = self.data[self.indx]
            arr_2 = self.data[self.indy]

        else:
            logger.error(
                " Distance matrix can be compute on 1-D and 2-D data tensors only"
            )
            raise ValueError

        results = []
        for first, second in zip(arr_1, arr_2):
            res = compute_earth_mover_dist(first, second)
            results.append(res)

        np_arr[self.indx, self.indy] = np.array(results)
        # Construct lower-triangle (it is a symmetric matrix)
        i_lower = np.tril_indices(len(self.data), -1)
        np_arr[i_lower] = np_arr.T[i_lower]
        logger.info(" Constructed entire distance matrix")

        return np_arr

    def _compute_distances_new_data_parallel(
        self, new_data, metric="emd", n_proc=cpu_count()
    ):
        """Compute distances for new data tensor.

        Parameters
        ----------
        new_data : np.ndarray
            Data tensor to classify.
        metric : str, optional
            Metric to be used. Defaults to EMD.
        n_proc : int, optional
            Number of processes. Defaults to cpu_count().

        """
        self.new_data = new_data

        if metric == "emd":
            dist_proc = self._emd_proc_new_data
        else:
            logger.error(" Only EMD metric implemented.")
            raise ValueError

        try:
            from progress.bar import Bar

            progress_module = True

        except ImportError:
            progress_module = False

        # 1-D array to fill with distances
        dist_arr = np.zeros(self.n)

        if progress_module:
            bar = Bar("Calculating distances... ", max=self.n / self.k_step_new_data)

        with Pool(n_proc) as pool:
            for k1, k2, res in pool.imap_unordered(
                dist_proc, range(0, self.n, self.k_step_new_data)
            ):
                dist_arr[k1:k2] = res

                if progress_module:
                    bar.next()
                else:
                    continue

        if progress_module:
            bar.finish()

        logger.info(" Computed distances for new data")
        return dist_arr

    def compute_distance_matrix(self, parallel=True, metric="emd", n_proc=cpu_count()):
        """
        Compute EMD distance matrix in parallel

        Parameters
        ----------
        metric : str, optional
            Metric to be used. Defaults to EMD.
        n_proc : int, optional
            Number of processes. Defaults to cpu_count().

        Returns
        ----------
        dist_matrix : np.ndarray
            NxN distance matrix
        """
        if parallel:
            dist_matrix = self._compute_distance_matrix_parallel()
        else:
            dist_matrix = self._compute_distance_matrix_serial()

        return dist_matrix

    def classify_new_data(self, new_data, top=10):
        """
        Classify new data by finding top smallest EMD distances.

        Parameters
        ----------
        new_data : np.ndarray
            Data tensor to classify (tested only with 2-D)
        top : int, optional
            top distances

        Returns
        ----------
        inds_arr : np.ndarray
            array containing indexes of top closest data to new_data
        dist_arr : np.ndarray
            array containing all the EMD distances

        """

        dist_arr = self._compute_distances_new_data_parallel(new_data=new_data)

        # select indexes of top distances
        inds_arr = np.argsort(dist_arr)[:top]

        return inds_arr, dist_arr
