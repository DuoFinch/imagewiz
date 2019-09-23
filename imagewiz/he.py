
#Helper functions that don't have much to do with image processing but facilitate other methods in this module


class sup:
    """Support class for handling tuples"""
    def __init__(self, tuples_, point):
        self.list_of_tuples = tuples_
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

#class helper