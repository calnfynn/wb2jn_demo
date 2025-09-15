Demo version of the WB2JN project. 

---

## CPS Coffeebook

(See also https://wiki.kewl.org/projects:coffeebook -- this is the same documentation with a few changes.)

This Quarto publising demo performs user defined SPARQL queries to generate Quarto markdown for use in demo documents.

This project depends on CPS Impress.

### CPS

CPS tools have been written for and provided by the CPS (Computational Publishing Service) as part of NFDI4Culture hosted at Wikibase4Research at TIB.

*CPS Ceiling Paintings
CPS Coffeebook
CPS Impress
CPS Selenium GET
CPS Wikibase*

### Setup

#### Debian

    sudo apt install build-essential python3-full python3-pip git
    git clone https://gitlab.com/nfdi4culture/computational-publishing-service/cps_coffeebook
    cd cps_coffeebook
    make venv

##### BASH

    source ~/.venvs/cps_coffeebook/bin/activate
    make install

### Create Environment / .env

Create three files called *.env*. 

One in the root directory (*cps_coffeebook/.env*):

    WB_URL="https://wikibase.kewl.org/"
    WB_USERNAME="username"
    WB_PASSWORD="botpass"

    SPARQL_URL="https://query.example.com/sparql"
    SPARQL_PREFIX="PREFIX wd: <https://wikibase.kewl.org/entity/>
    PREFIX wdt: <https://wikibase.kewl.org/prop/direct/>
    PREFIX p: <https://wikibase.kewl.org/prop/>
    PREFIX ps: <https://wikibase.kewl.org/prop/statement/>
    PREFIX pq: <https://wikibase.kewl.org/prop/qualifier/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>"

    PROJECT_DIR="./Impress"
    CACHE_DIR="./Quarto"

    LOGGING="CRITICAL"

One in the Quarto directory (*cps_coffeebook/Quarto/.env*):

    WB_URL="https://wikibase.kewl.org/"
    WB_USERNAME="username"
    WB_PASSWORD="botpass"

    SPARQL_URL="https://query.example.com/sparql"
    SPARQL_PREFIX="PREFIX wd: <https://wikibase.kewl.org/entity/>
    PREFIX wdt: <https://wikibase.kewl.org/prop/direct/>
    PREFIX p: <https://wikibase.kewl.org/prop/>
    PREFIX ps: <https://wikibase.kewl.org/prop/statement/>
    PREFIX pq: <https://wikibase.kewl.org/prop/qualifier/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>"

    PROJECT_DIR="../Impress"
    CACHE_DIR="."

    LOGGING="CRITICAL"

And one in the Notebook directory (*cps_coffeebook/Notebook/.env*):

    WB_URL="https://wikibase.kewl.org/"
    WB_USERNAME="username"
    WB_PASSWORD="botpass"

    SPARQL_URL="https://query.example.com/sparql"
    SPARQL_PREFIX="PREFIX wd: <https://wikibase.kewl.org/entity/>
    PREFIX wdt: <https://wikibase.kewl.org/prop/direct/>
    PREFIX p: <https://wikibase.kewl.org/prop/>
    PREFIX ps: <https://wikibase.kewl.org/prop/statement/>
    PREFIX pq: <https://wikibase.kewl.org/prop/qualifier/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>"

    PROJECT_DIR="../Impress"
    CACHE_DIR="../Quarto"

    LOGGING="CRITICAL"

An environment file .env is used to contain configuration data. See “dotenv” for details.

### Project

The cps_impress project directory contains project subdirectories each with at least two files:

*query.py
template.j2* 

The query.py file has two methods, one to return the SPARQL query string for CPS Impress and the other to filter the SPARQL query results.

The template file is any name with a j2 extention and this is a Jinja2 template file.

### Notebook

The notebook directory contains jupyter-notebook project files demonstrating queries and templates visually.

    make notebook
    
You might need to refresh your browser page if it seems to get stuck. 

Open new terminal. Start the .venv again:

    source ~/.venvs/cps_coffeebook/bin/activate

### Quarto

This directory contains Quarto project to generate documents in docx and PDF format.

    cd Quarto

Initially you may require Latex support to be installed, this can be achieved by entering: [[1]](#1)

    make setup

To generate the demo documents, enter make (Jupyter Notebooks needs to be running for this):

    make


##### 1

IF you get an error during *make setup*/TinyTex install:

    sudo add-apt-repository universe
    sudo apt-get update
    sudo apt-get texlive-latex-base

And add the following in *Quarto/_quarto.yml*:

    format:
      pdf:
        pdf-engine: pdflatex
        
---

## Quarto Publish

(See also [Quarto Documentation](https://quarto.org/docs/publishing/github-pages.html).)

### Render to \../docs

#### Set source

On GitHub, set your website to render from the *docs* directory of the main branch.

![](https://quarto.org/docs/publishing/images/gh-pages-docs-dir.png)

In *_quarto.yml* add this:

    project:
      output-dir: ../docs
      
#### Ignoring output 

Still in your root directory, add `Quarto/_book/` to *.gitignore*.

Then go to the Quarto directory and add a *.nojekyll* file.

    cd Quarto
    touch .nojekyll

### Publishing 

#### Render & push 

Render and push to GitHub.

    make
    git add ../docs 
    git add _quarto.yml
    git commit -m "Publish site to Docs/"
    git push
    
#### *gh-pages* branch
Initialise a *gh-pages* branch, then go back to your main branch.
    
    git checkout --orphan gh-pages
    git reset --hard # make sure all changes are committed before running this!
    git commit --allow-empty -m "Initialising gh-pages branch"
    git push origin gh-pages

    git checkout main
    
#### Change source

Go back to the GitHub page settings and change the source to the root of the *gh-pages* branch.

![](https://quarto.org/docs/publishing/images/gh-pages-user-site.png)
    
#### Run publish command 

In your Quarto directory, run the publish command: 

    quarto publish gh-pages
