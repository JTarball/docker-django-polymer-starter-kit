#!/usr/bin/env python
'''
    stats.views
    ===========
'''
import logging

from django.http import HttpResponseBadRequest

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from stats import redis_stat

logger = logging.getLogger('project_logger')

rs = redis_stat.redis_stat()

# Line Graph
# Produces a chartist.js line graph script
@api_view(['GET'])
@permission_classes((AllowAny, ))
def line_graph_view(request):
    """ Produces Line Graph. """
    # Allow Maximum of 5 series of data
    series1 = request.GET.get('series1', "")
    logger.info("%s" % series1)
    series2 = request.GET.get('series2', "")
    series3 = request.GET.get('series3', "")
    series4 = request.GET.get('series4', "")
    series5 = request.GET.get('series5', "")
    # Start / End Date / Freq & Any Other Config
    axisxtitle = request.GET.get("axisxtitle", " ")
    axisytitle = request.GET.get("axisytitle", " ")
    start = request.GET.get('start', "")
    end = request.GET.get('end', "")
    freq = request.GET.get('freq', "")
    show_area = request.GET.get('showArea', "false")
    if freq == "" or start == "" or end == "" or series1 == "":
        return HttpResponseBadRequest()
    # Get Data from Redis
    data_series1 = None
    data_series2 = None
    data_series3 = None
    data_series4 = None
    data_series5 = None
    # Ugly but works
    # We need at least one series
    data_series1 = rs.get(series1, start, end, freq)
    if series2 != "":
        data_series2 = rs.get(series2, start, end, freq)
    if series3 != "":
        data_series3 = rs.get(series3, start, end, freq)
    if series4 != "":
        data_series4 = rs.get(series4, start, end, freq)
    if series5 != "":
        data_series5 = rs.get(series5, start, end, freq)
    # Create x labels for graph
    str_labels = ""
    for label in data_series1.index:
        str_labels += "'%s'," % label
    # Again ugly but works - create series string for script (name and data)
    str_series = ""
    if data_series1 is not None:
        str_series += "{ name: '%s', data: [0," % "Series 1"
        for count in data_series1['count']:
            if str(count) == 'nan':
                count = "null"
            str_series += "%s," % count
        str_series += "] },"
    if data_series2 is not None:
        str_series += "{ name: '%s', data: [" % "Series 2"
        for count in data_series2['count']:
            if str(count) == 'nan':
                count = "null"
            str_series += "%s," % count
        str_series += "] },"
    if data_series3 is not None:
        str_series += "{ name: '%s', data: [" % "Series 3"
        for count in data_series3['count']:
            if str(count) == 'nan':
                count = "null"
            str_series += "%s," % count
        str_series += "] },"
    if data_series4 is not None:
        str_series += "{ name: '%s', data: [" % "Series 4"
        for count in data_series4['count']:
            if str(count) == 'nan':
                count = "null"
            str_series += "%s," % count
        str_series += "] },"
        str_series += "{ name: '%s', data: [" % "Series 5"
    if data_series5 is not None:
        for count in data_series5['count']:
            if str(count) == 'nan':
                count = "null"
            str_series += "%s," % count
        str_series += "] },"
    # Create chartist.js line graph with options
    graph_script = ("new Chartist.Line('.ct-chart', "
                    "{ labels: [%s] , "
                    "series: [%s]}, "
                    "{ fullWidth: true, chartPadding: { right: 40 }, showArea: %s, "
                    """plugins: [
                    Chartist.plugins.ctAxisTitle({
                        axisX: {
                            axisTitle: '%s',
                            axisClass: 'ct-axis-title',
                            offset: {
                                x: 0,
                                y: 50
                            },
                            textAnchor: 'middle'
                        },
                        axisY: {
                            axisTitle: '%s',
                            axisClass: 'ct-axis-title',
                            offset: {
                                x: 0,
                                y: -1
                            },
                            flipTitle: false
                        }
                    })
                    ]"""
                    " });") % (str_labels, str_series, show_area, axisxtitle, axisytitle)
    return Response("%s" % graph_script)


# Bar Graph
@api_view(['GET'])
def bar_graph_view(request):
    """ Produces Line Graph. """
    q = request.GET.get('q', "")
    logger.info("autosuggest_view   q ----------- %s" % q)
    return Response("<script>parent.Response_OK();</script>")

# stat_field, start_date, end_date, freq

# stat=[<stat1>, <stat2>, <stat3>]



