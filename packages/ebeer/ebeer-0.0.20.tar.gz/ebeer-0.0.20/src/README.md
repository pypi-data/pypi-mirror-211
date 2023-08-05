# ebeer - pre-trained CNN

CNN Trained to predict brazilian beers


## Example implementation

```

import ebeer

n_pos = ebeer.BeerClassifier.predict("assets/beer_imgs/0.jpg")

print("Label:", ebeer.DataLabel[n_pos]["name"])

```

## Simple example implementation

```

import ebeer

beerData = ebeer.BeerClassifier.predict_simple(
    "assets/beer_imgs/0.jpg")

print('beerData:', beerData)

```