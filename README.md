# Lingtrain Alignment Studio

![asd](/img/title.jpg)

## Intro

Lingtrain Alignment Studio is the ML based app for accurate texts alignment on different languages.

- Extracts parallel corpora from two texts.
- Makes the formatted parallel book from it with sentence highlightning.

## Models

Automated alignment process relies on the sentence embeddings models. Embeddings are multidimensional vectors of a special kind which are used to calculate a distance between the sentences. You can also plug your own model using the interface described in models directory. Supported languages list depend on the selected backend model.

- **distiluse-base-multilingual-cased-v2**
  - more reliable and fast
  - moderate weights size — 500MB
  - supports 50+ languages
  - full list of supported languages can be found in [this paper](https://arxiv.org/abs/2004.09813)
- **LaBSE (Language-agnostic BERT Sentence Embedding)**
  - can be used for rare languages
  - pretty heavy weights — 1.8GB
  - supports 100+ languages
  - full list of supported languages can be found [here](https://arxiv.org/abs/2007.01852)

## Running on local machine

You can run the application on your computer using docker.

1. Make sure that docker is installed by typing the <code>docker version</code> command in your console.
2. Images configured to run locally are available on Docker Hub.

3. Run the following commads in your console:
<code>docker pull lingtrain/aligner:v4</code>
<code>docker run -p 80:80 lingtrain/aligner:v4</code>

4. App will be available in your browser on the <code>localhost</code> address.

## Running in development mode

Clone this repo on your machine.

### Backend

Flask/uwsgi backend REST API service. It's pretty simple and contains all the alignment logic.

<code>cd /be</code>
<code>python main.py</code>

### Frontend

SPA. Vue + vuex + vuetify. UI for managing alignment process using BE and a tool for translators to edit processing documents.

<code>cd /fe</code>

#### Setup

<code>npm install</code>

#### Compile and run with hot-reloads for development

<code>npm run serve</code>

## Feedback

You can crate an issue or send me a message in telegram: @averkij

## License

This work is licensed under a [Attribution-NonCommercial-NoDerivatives 4.0 International](http://creativecommons.org/licenses/by-nc-nd/4.0/) license. See LICENSE.

<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a>
