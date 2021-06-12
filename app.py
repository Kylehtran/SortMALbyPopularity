from flask import Flask, render_template, request, url_for, flash, redirect
import requests
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter
import os

from Forms import Usernameform, SearchPage
from AnimeEntry import AnimeEntry
from getUserList import sortListbyPopularity, getSortedList, sortByStatusList

app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def form():
    form = Usernameform()
    if request.method == 'POST':
        sortListbyPopularity(form.username.data)
        return redirect( url_for('list', username = form.username.data, selected_status = "All")) 
    
    return render_template('getUsername.html', form = form)


@app.route('/list/<username>/<selected_status>', methods=['GET', 'POST'])
def list(username, selected_status):

    searchPage = SearchPage()
    if not getSortedList():
        return redirect( url_for('error'))

    if(selected_status == "All"):
        sortedList = getSortedList()
    else:
        sortedList = sortByStatusList(selected_status)

    PER_PAGE =10

    statuses = ["All", "Watching", "Completed", "Dropped", "On Hold", "Plan To Watch"]

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    
    if request.method == "POST":
        if request.form.get("anime_status") in statuses:
            selected_status = request.form.get("anime_status")
            return redirect( url_for('list', username = username, selected_status = selected_status)) 
        else:
            try:
                if int(searchPage.search.data) <= (len(sortedList)/10):
                    page = int(searchPage.search.data)
                elif ((int(searchPage.search.data) % 10) > 0) and (int(searchPage.search.data) <=  (len(sortedList)/10)+1):
                    page = int(searchPage.search.data)
                else:
                    page = page
            except:
                page = page

    i=(page-1)*PER_PAGE
    List1=sortedList[i:i+10]
    pagination = Pagination(page=page, total = len(sortedList), per_page = PER_PAGE, record_name = username + ' \'s Anime List', css_framework='bootstrap4')

    
    
    
    return render_template('displayList.html', len = len(List1), sortedList = List1, pagination = pagination, anime_status=statuses, selected_status = selected_status, username = username, searchPage = searchPage)

@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template('error.html')

if __name__ == '__main__':

    app.run()



    
  