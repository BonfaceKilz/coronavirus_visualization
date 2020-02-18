from plotly.graph_objects import Scattergeo, Figure

import plotly.offline as go_offline
import pandas as pd

URL = 'https://docs.google.com/spreadsheets/d/18X1VM1671d99V_yd-cnUI1j8oSG2ZgfU_q1HfOizErA/export?format=csv&id'


class Grapher():
    def __init__(self, url):
        self.url = url
        self.data = pd.read_csv(self.url).fillna(0)


    def create_graph(self):
        fig = Figure()

        date_list = []
        for confirmed_case_date, death_date in zip(self.data.filter(like='confirmedcases'),
                                                   self.data.filter(like='deaths')):
            df = self.data[
                ['latitude',
                 'longitude',
                 'country',
                 'location',
                 confirmed_case_date,
                 death_date,
                 ]
            ]
            date_list.append(death_date[-10:])
            df_cases = df[df[confirmed_case_date] != 0]
            df_cases['text'] = (df_cases['country']
                                + '<br>'
                                + df_cases['location']
                                + '<br>'
                                + 'confirmed cases: '
                                + (df_cases[df_cases.columns[-2]].astype(int)).astype(str)
                                + '<br>'
                                + 'deaths: '
                                + (df_cases[df_cases.columns[-1]].astype(int)).astype(str))

            df_deaths = df[df[death_date] != 0]
            df_deaths['text'] = (df_deaths['country']
                                 + '<br>'
                                 + df_deaths['location']
                                 + '<br>' + 'confirmed cases: '
                                 + (df_deaths[df_deaths.columns[-2]].astype(int)).astype(str)
                                 + '<br>'
                                 + 'deaths: '
                                 + (df_deaths[df_deaths.columns[-1]].astype(int)).astype(str))

            fig.add_trace(Scattergeo(name='Infections',
                                        lon=df_cases['longitude'],
                                        lat=df_cases['latitude'],
                                        visible=False,
                                        hovertemplate=df_cases['text'],
                                        text='Text',
                                        mode='markers',
                                        marker=dict(size=10, opacity=0.6, color='Blue', symbol='circle')))
            fig.add_trace(Scattergeo(name='Deaths',
                                        lon=df_deaths['longitude'],
                                        lat=df_deaths['latitude'],
                                        visible=False,
                                        hovertemplate=df_deaths['text'],
                                        text="Text",
                                        mode='markers',
                                        marker=dict(size=10, opacity=0.6, color='Red', symbol='circle')))

            steps = []
            for index, i in enumerate(range(0, len(fig.data), 2)):
                step = dict(
                    method="restyle",
                    args=["visible", [False] * len(fig.data)],
                    label=date_list[index],
                )
                step["args"][1][i] = True
                step["args"][1][i+1] = True
                steps.append(step)

            sliders = [dict(
                active=0,
                currentvalue={"prefix": "Date: "},
                pad={"t": 1},
                steps=steps
            )]

            fig.data[0].visible = True
            fig.data[1].visible = True

        fig.update_geos(
            showcountries=True, countrycolor="RebeccaPurple",
            projection_type='natural earth'
        )
        fig.update_layout(sliders=sliders,
                          title='Rise of the Novel Coronavirus<br>A Python Data Visualization by Advait Joshi', title_x=0.5,
                          legend_title='Key',
                          height=600)
        fig.show()
        go_offline.plot(fig, filename='./map_cov.html',
                        validate=True, auto_open=False
                        )


if __name__ == "__main__":
    grapher = Grapher(url=URL)
    grapher.create_graph()
