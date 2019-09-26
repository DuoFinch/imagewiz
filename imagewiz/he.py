
#Helper functions that don't have much to do with image processing but facilitate other methods in this module


class sup:
    """Support class for handling tuples"""
    def __init__(self, tuples_):
        self.list_of_tuples = tuples_

        #make this the starting point, the median of the x plane and the median of the y plane
        self.point = point

    def iterator(self, method="No-Repeat"):
        if method == "No-Repeat":
            final_index_list = list()
            for i in range(0, len(self.list_of_tuples)):
                for x in range(i + 1, len(self.list_of_tuples)):
                    temp_tuple = (i, x)
                    final_index_list.append(temp_tuple)

        elif method == "Repeat":
            final_index_list = list()
            for i in range(0, len(self.list_of_tuples)):
                for x in range(0, len(self.list_of_tuples)):
                    if i == x:
                        pass
                    else:
                        final_index_list.append((i, x))
        else:
            print("Method not recognized!")
        return final_index_list


    def mean_absoulte_deviation_xy(self, verbose=True):
        """We must ensure that we only compute each pair once"""

        deviations = []
        mean = lambda list_x: sum(list_x) / len(list_x)

        if verbose:
            for i in tqdm.tqdm(iterator(self.list_of_tuples)):
                point_1 = self.list_of_tuples[i[0]]
                point_2 = self.list_of_tuples[i[1]]

                # Pythagoras theorem
                dist = ((point_2[0] - point_1[0]) ** 2) + ((point_2[1] - point_1[1]) ** 2)
                sq_dist = math.sqrt(dist)
                deviations.append(sq_dist)

        elif not verbose:
            for i in iterator(self.list_of_tuples):
                point_1 = self.list_of_tuples[i[0]]
                point_2 = self.list_of_tuples[i[1]]

                dist = ((point_2[0] - point_1[0]) ^ 2) + ((point_2[1] - point_1[1]) ^ 2)
                sq_dist = math.sqrt(dist)
                deviations.append(sq_dist)

        # Mean of all distances
        means_dists = mean(deviations)

        return means_dists

    def sum_of_deviations(self):
        deviations = []
        for i in iterator(self.list_of_tuples):
            point_1 = self.list_of_tuples[i[0]]
            point_2 = self.point

            # Pythagoras theorem
            dist = ((point_2[0] - point_1[0]) ** 2) + ((point_2[1] - point_1[1]) ** 2)
            sq_dist = math.sqrt(dist)
            deviations.append(sq_dist)

        # Mean of all distances
        result = sum(deviations)

        return result

    def apr_median_weis(list_of_tuples, P):
        """Weiszfeld algorithm method"""
        # Apply one iteration of algorithm
        W = 0.0
        x_ = 0
        y_ = 0
        for q in list_of_tuples:

            # Pythagoras theorem
            dist = ((P[0] - q[0]) ** 2) + ((P[1] - q[1]) ** 2)
            d = math.sqrt(dist)

            # Adaptation to zero distancing
            if d != 0:
                x_ += q[0] / d
                y_ += q[1] / d
                w = 1.0 / d
                W += w

        return (x_ / W, y_ / W)

    def geo_med_weis(list_of_tuples, epsilon=0.001, starting_point="medianx,mediany"):
        """Weiszfeld algorithm method"""
        if starting_point == "medianx,mediany":
            # Instantiate by creating a starting point at the median of each plane
            list_x = []
            list_y = []

            for p in list_of_tuples:
                tx = p[0]
                ty = p[1]
                list_x.append(tx)
                list_y.append(ty)

            initial_P = (median(list_x), median(list_y))
        else:
            initial_P = starting_point

        _result = apr_median_weis(list_of_tuples, initial_P)
        _dev = sum_of_deviations(list_of_tuples, initial_P)

        curr_point = _result
        curr_ep = epsilon + 1

        placeholder = 0

        while curr_ep > epsilon:
            if placeholder > 0:
                _dev = new_dev
                optimized_point = apr_median_weis(list_of_tuples, optimized_point)

                new_dev = sum_of_deviations(list_of_tuples, optimized_point)

                # Difference is all we care about here
                curr_ep = abs(abs(_dev) - abs(new_dev))

            else:
                new_point = apr_median_weis(list_of_tuples, curr_point)
                new_dev = sum_of_deviations(list_of_tuples, new_point)
                curr_ep = abs(abs(_dev) - abs(new_dev))
                optimized_point = new_point
                placeholder += 1

        return optimized_point

#class helper