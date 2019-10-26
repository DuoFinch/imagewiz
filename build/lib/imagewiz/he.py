
import numpy as np
import tqdm
import math


class sup:
    """Support class for handling tuples"""

    def __init__(self, tuples_):
        self.list_of_tuples = tuples_

        # Instantiate by creating a starting point at the median of each plane
        list_x = []
        list_y = []

        for p in self.list_of_tuples:
            tx = p[0]
            ty = p[1]
            list_x.append(tx)
            list_y.append(ty)

        self.point = (np.median(list_x), np.median(list_y))

        # Storage for index list
        self.it_list = None

        # Last sum of deviations
        self.lastdev = None

    def iterator(self, repeat=False):
        """Creates an index of items in a list to iterate over.
        This function will either create a list that removes truly duplicated functions or not
        depends on the selected method"""
        if not repeat:
            final_index_list = list()
            for i in range(0, len(self.list_of_tuples)):
                for x in range(i + 1, len(self.list_of_tuples)):
                    temp_tuple = (i, x)
                    final_index_list.append(temp_tuple)

        elif repeat:
            final_index_list = list()
            for i in range(0, len(self.list_of_tuples)):
                for x in range(0, len(self.list_of_tuples)):
                    if i == x:
                        pass
                    else:
                        final_index_list.append((i, x))
        else:
            print("Method not recognized!")

        self.it_list = final_index_list

        return self.it_list

    def mean_absoulte_deviation_xy(self, verbose=True):
        """We must ensure that we only compute each pair once"""

        deviations = []
        mean = lambda list_x: sum(list_x) / len(list_x)

        if verbose:
            for i in tqdm.tqdm(sup(self.list_of_tuples).iterator()):
                point_1 = self.list_of_tuples[i[0]]
                point_2 = self.list_of_tuples[i[1]]

                # Pythagoras theorem
                dist = ((point_2[0] - point_1[0]) ** 2) + ((point_2[1] - point_1[1]) ** 2)
                sq_dist = math.sqrt(dist)
                deviations.append(sq_dist)

        elif not verbose:
            for i in sup(self.list_of_tuples).iterator():
                point_1 = self.list_of_tuples[i[0]]
                point_2 = self.list_of_tuples[i[1]]

                dist = ((point_2[0] - point_1[0]) ** 2) + ((point_2[1] - point_1[1]) ** 2)
                sq_dist = math.sqrt(dist)
                deviations.append(sq_dist)

        # Mean of all distances
        means_dists = mean(deviations)

        return means_dists

    def sum_of_deviations(self):
        """Sum of distances from self.point to every item in list of tuples """
        deviations = []
        for i in self.it_list:
            point_1 = self.list_of_tuples[i[0]]

            # Pythagoras theorem
            dist = ((self.point[0] - point_1[0]) ** 2) + ((self.point[1] - point_1[1]) ** 2)
            sq_dist = math.sqrt(dist)
            deviations.append(sq_dist)

        # Mean of all distances

        self.lastdev = sum(deviations)

        return self.lastdev

    def apr_median_weis(self):
        """Weiszfeld algorithm method"""
        # Apply one iteration of algorithm
        W = 0.0
        x_ = 0
        y_ = 0
        for q in self.list_of_tuples:

            # Pythagoras theorem
            dist = ((self.point[0] - q[0]) ** 2) + ((self.point[1] - q[1]) ** 2)
            d = math.sqrt(dist)

            # Adaptation to zero distancing
            if d != 0:
                x_ += q[0] / d
                y_ += q[1] / d
                w = 1.0 / d
                W += w

        self.point = (x_ / W, y_ / W)

        return self.point

    def geo_med_weis(self, epsilon=0.001):
        """Weiszfeld algorithm method"""

        _dev = self.sum_of_deviations()

        # Initial epsilon that will not end next while loop before it is run
        curr_ep = epsilon + 1

        placeholder = 0

        while curr_ep > epsilon:
            self.apr_median_weis()
            curr_ep = abs(_dev - self.sum_of_deviations())
            _dev = self.sum_of_deviations()

        return self.point
