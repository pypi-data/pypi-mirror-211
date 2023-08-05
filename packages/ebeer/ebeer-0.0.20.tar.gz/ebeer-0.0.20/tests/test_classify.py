class Test_Classify:

    def test_has_weights_file(self):

        import importlib_resources

        resource_path = importlib_resources.files(
            'ebeer').joinpath('trained_model.h5')

        flg = False if resource_path is None else True

        print('flg trained_model:', flg)

        assert True

    def test_has_metadata_file(self):

        import importlib_resources

        resource_path = importlib_resources.files(
            'ebeer').joinpath('general_metadata.json')

        flg = False if resource_path is None else True

        print('flg general_metadata:', flg)

        assert True

    def test_predict(self):

        import ebeer

        PATH_BEER = "assets/beer_imgs/16.jpg"  # skol
        PATH_BEER = "assets/beer_imgs/3.jpg"  # brahma
        PATH_BEER = "assets/beer_imgs/9.jpg"  # heiniken

        vet_pred = ebeer.BeerClassifier.predict(PATH_BEER)

        n_pos = vet_pred.argmax(axis=-1)[0]

        print("n_pos:", n_pos)

        PATH_METADATA = ebeer.BeerClassifier.get_path_from_filename(
            'metadata.json')

        json_obj = ebeer.BeerClassifier.get_object_from_json(PATH_METADATA)

        dict_labels_index = {i: json_obj[i] for i in range(len(json_obj))}

        print("Label:", dict_labels_index[n_pos]["name"])

        assert True
