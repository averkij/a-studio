# Lingtrain Studio

![asd](/img/title.jpg)

## 💡 Intro

Lingtrain Studio is the ML based app for accurate texts alignment on different languages.

- Extracts parallel corpora from two texts.
- Makes the formatted parallel book from it with sentence highlightning.

## ⚡ Articles

-  [How to create bilingual books. Part 2. Lingtrain Alignment Studio](https://medium.com/@averoo/how-to-create-bilingual-books-part-2-lingtrain-alignment-studio-ffa56c9c07a6)
-  [How to make a parallel texts for language learning. Part 1. Python and Colab version](https://medium.com/@averoo/how-to-make-a-parallel-book-for-language-learning-part-1-python-and-colab-version-cff09e379d8c)
-  [Lingtrain Aligner. Приложение для создания параллельных книг, которое вас удивит](https://habr.com/ru/post/564944/)
-  [Сам себе Гутенберг. Делаем параллельные книги](https://habr.com/ru/post/557664/)

## 🧬 Models

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

## 💻 Running on local machine

You can run the application on your computer using docker.

1. Make sure that docker is installed by typing the <code>docker version</code> command in your console.

2. Images configured to run locally are available on Docker Hub.

3. Run the following commads in your console:
    - <code>docker pull lingtrain/studio:v7.2</code>
    - <code>docker run -v C:\app\data:/app/data -v C:\app\img:/app/static/img -p 80:80 lingtrain/studio:v7.2</code>

4. App will be available in your browser on the <code>localhost</code> address.

5. If you need to run the container on another port (e.g. localhost:8081):
    - Change the API_URL parameter in config.js
    - Rebuild the docker container
    - Start it with changed -p parameter (e.g. -p 8081:80)

## 🔨 Running in development mode

Clone this repo on your machine.

### Backend

Flask/uwsgi backend REST API service. It contains all the alignment logic.

- Go to the backend directory
  - <code>cd /backend</code>

- Install the requirements
  - <code>pip install -r requirements.txt</code>

- Run the backend application
  - <code>python main.py</code>

### Frontend

SPA. Vue + vuex + vuetify. UI for managing alignment process using BE and a tool for translators to edit processing documents.

- Go to the backend directory
  - <code>cd /frontend</code>

- Install the requirements
  - <code>npm install -f</code>

- Compile and run with hot-reloads for development
  - <code>npm run serve</code>

Application will be available on <code>localhost:8080</code>

## ✉️ Feedback

You can crate an issue or send me a message in telegram: @averkij

## 🔑 License

This work is licensed under a [Attribution-NonCommercial-NoDerivatives 4.0 International](http://creativecommons.org/licenses/by-nc-nd/4.0/) license. See LICENSE.

<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a>
