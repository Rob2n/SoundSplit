# SoundSplit
#### Track splitting for everyone
***
## What made SoundSplit possible

This project was made possile after Deezer released a Proof of Concept project called [Spleeter](https://github.com/deezer/spleeter)

It is a really powerful but hard-to-use machine learning model that is able to split music tracks (separate intrumental from vocals for example) 

## What we did

After a lot of research on the inner workings of the model, we retrained the last layer of the Spleeter model on [this dataset](http://mac.citi.sinica.edu.tw/ikala/index.html) to bring more diversity to the model training (they previously trained on [MUSBD and a private music dataset](https://arxiv.org/pdf/1906.02618.pdf))

## The project

The final objective was to make an easy-to-use and efficient track splitting model and make it super simple to use, even for untrained users.

We created a website capable of processing music files, serving them to our pretrained model, and serving the split tracks after the splitting process was done.

***
### Developpment tips

To start the developpment server, just run server/run.sh
