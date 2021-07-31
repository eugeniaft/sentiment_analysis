import plotly.express as px
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from datetime import datetime

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')


def text_sentiment(text):
    doc = nlp(text)
    polarity = doc._.polarity
    return polarity


def format_date(date):
    
    new_dt = datetime.strftime(datetime.strptime(date, 
                                                 '%a %b %d %H:%M:%S +0000 %Y'), 
                               '%Y-%m-%d %H:%M:%S')
    return new_dt


def data_for_analysis(data):
    data['created_at_dt'] = data['created_at'].apply(lambda x: format_date(x))
    data = data.sort_values('created_at_dt').reset_index(drop=True)
    data['polarity'] = data['text'].apply(lambda x: text_sentiment(x))
    return data

def line_plot(data, x, y, c, ylab, title):

    fig = px.scatter(data, x, y, title=title, template="ggplot2")
    fig.update_traces(line_color=c)

    fig.update_layout(
        height=500,
        width=750,
        yaxis=dict(
            title=ylab,
            ),
        xaxis={'title': '',
               'type': 'category'
              }
        )
    return fig
