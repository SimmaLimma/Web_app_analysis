import json
import plotly

def data_to_graph_json(goal_diffs, goals_on_matches):
    """
    Makes the pandas dataframes returned from
    PLData.get_goal_diffs() and
    PLData.get_scatter_goal_data()
    to format readable by plotly in frontend.
    Also makes it to JSON, so sending it to front end is easy
    """

    # List of graphs that will be used in front end. 
    # First graph is of goal differences between teams
    # and is plotted as a bar graph.
    # Second graph is bubble chart on how many matches that ended
    # with a specific result
    graphs = [
        dict(
            data=[
                dict(
                    x=goal_diffs.index,
                    y=goal_diffs,
                    type='bar'
                ),
            ],
            layout=dict(
                title='Goal differences',
                yaxis=dict(
                    title='Mean goal difference'
                ),
                xaxis=dict(
                    title='Team(s)'
                )
            )
        ), 
        dict(
            data=[
                dict(
                    x=goals_on_matches.x,
                    y=goals_on_matches.y,
                    type='scatter',                        
                    mode='markers',
                    marker=dict(
                        size=goals_on_matches.bubble_sizes
                    )
                ),
            ],
            layout=dict(
                title='Amount of matches with specific result.',
                yaxis=dict(
                    title='Made goals'
                ),
                xaxis=dict(
                    title='Conceded goals'
                )
            )
        )
    ]

    return json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)