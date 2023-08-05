import time
import edaplore.interactions.interactions_classes as inter_class

class ComparatorU:
    def __init__(self, separ, cols):
        """
        Initializes the ComparatorU class, creates instances of interactions between numeric, categorical and boolean data.

        :param separ: An instance of Separator class.
        :param cols: A list of column names to consider for interactions.
        """
        self.storage = {}
        self.cols = cols
        self.allowed_cols = set()
        full_time = time.time()
        nn_time = time.time()
        for el1 in separ.numeric_list:
            if el1.column_name in cols:
                for el2 in separ.numeric_list:
                    if el2.column_name in cols:
                        if el1 is el2:
                            self.storage[f'{el1.column_name}_{el1.column_name}'] = el1.rendered
                            self.allowed_cols.add(el1.column_name)
                        else:
                            inter = inter_class.NumNum(el1, el2)
                            self.allowed_cols.add(el1.column_name)
                            self.allowed_cols.add(el2.column_name)
                            self.storage[inter.name] = inter.rendered
        print(f'===nn loop {time.time() - nn_time}')
        nn_time = time.time()

        for el1 in separ.numeric_list:
            if el1.column_name in cols:
                for el2 in separ.categorical_list + separ.boolean_list:
                    if el2.column_name in cols and el2.count_categories <= 3:
                        inter = inter_class.NumCat(el1, el2)
                        self.allowed_cols.add(el1.column_name)
                        self.allowed_cols.add(el2.column_name)
                        self.storage[inter.name] = inter.rendered
        print(f'===nc loop {time.time() - nn_time}')
        nn_time = time.time()
        for el1 in separ.categorical_list + separ.boolean_list:
            if el1.column_name in cols and el1.count_categories <= 3:
                for el2 in separ.categorical_list + separ.boolean_list:
                    if el2.column_name in cols and el2.count_categories <= 3:
                        if el1 is el2:
                            self.allowed_cols.add(el1.column_name)
                            self.storage[f'{el1.column_name}_{el1.column_name}'] = el1.rendered
                        else:
                            self.allowed_cols.add(el1.column_name)
                            self.allowed_cols.add(el2.column_name)
                            inter = inter_class.CatCat(el1, el2)
                            self.storage[inter.name] = inter.rendered
        print(f'===cc loop {time.time() - nn_time}')
        nn_time = time.time()
        for el1 in separ.numeric_list:
            if el1.column_name in cols:
                for el2 in separ.numeric_list:
                    if el2.column_name in cols and not (el1 is el2):
                        for el3 in separ.categorical_list + separ.boolean_list:
                            if el3.column_name in cols and el3.count_categories <= 3:
                                self.allowed_cols.add(el1.column_name)
                                self.allowed_cols.add(el2.column_name)
                                self.allowed_cols.add(el3.column_name)
                                inter = inter_class.Num2Cat(el1, el2, el3)
                                self.storage[inter.name] = inter.rendered
        print(f'===n2c loop {time.time() - nn_time}')
        nn_time = time.time()
        for el1 in separ.numeric_list:
            if el1.column_name in cols:
                for el2 in separ.categorical_list + separ.boolean_list:
                    if el2.column_name in cols and el2.count_categories <= 3:
                        for el3 in separ.categorical_list + separ.boolean_list:
                            if el3.column_name and not (el2 is el3) and el3.count_categories <= 3:
                                self.allowed_cols.add(el1.column_name)
                                self.allowed_cols.add(el2.column_name)
                                self.allowed_cols.add(el3.column_name)
                                inter = inter_class.NumCat2(el1, el2, el3)
                                self.storage[inter.name] = inter.rendered
        print(f'===nc2 loop {time.time() - nn_time}')
        nn_time = time.time()
        self.cols = list(self.allowed_cols)
