import json

from django.http import HttpResponse
from django.shortcuts import render
from neomodel import Q

from .models import Country
from .utils import (fetch_nodes, fetch_countries, filter_countries)

from rest_framework.views import APIView
from rest_framework.response import Response


def get_suggestions(request):
    print("hey")
    if request.is_ajax():
        print("ajax correct")
        q = request.GET.get('term', '')
        print("term is " + q)
        places = filter_countries(q)
        # print("lent db " + str(places))

        results = []

        for node in places:
            # print(node[0])
            # place_json['label'] = node.name
            # place_json['value'] = pl.name
            if isinstance(node[0], int):
                print("here")
            else:
                # for type of the node
                node_type = ''
                labels = node[0][0].labels
                for l in labels:
                    node_type = l
                    print(node_type)

                node_properties = _get_node_properties(node[0][0])
                # if node_properties[node_type]
                found_property = node[0][1]
                print(node_properties[found_property] + " node")
                if node_type == 'Book':
                    if found_property != 'title':
                        place_json = {'value': node_properties[found_property] + ', ' + node_properties['title']}
                        results.append(place_json)
                for keyValue in node_properties:
                    # print(node_properties[keyValue])

                    place_json = {'value': node_properties[keyValue]}
                    # if q in node_properties[keyValue]:
                    #     if not results.__contains__(place_json):
                    # results.append(place_json)

        data = json.dumps(results)
    else:
        print("fail")
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_list(request, query_str):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}

    print("hey")
    if request.is_ajax():
        print("ajax correct")

        # data = json.dumps(results)
    else:
        print("fail")
        data = 'fail'
    mimetype = 'application/json'
    # q = request.GET.get('term', '')
    # print("term is " + q)
    places = filter_countries(query_str)
    # print("lent db " + str(places))

    results = []

    for node in places:
        # print(node[0])
        # place_json['label'] = node.name
        # place_json['value'] = pl.name
        if isinstance(node[0], int):
            print("here")
        else:
            node_properties = _get_node_properties(node[0])
            for keyValue in node_properties:
                # print(node_properties[keyValue])
                place_json = {'value': node_properties[keyValue]}
                # if q in node_properties[keyValue]:
                #     if not results.__contains__(place_json):
            results.append(node_properties)
            print(results)
            context = {'results': results}
    return render(request, 'detail.html', context)


# for pl in places:
#     place_json = {}
#     place_json['label'] = pl.name
#     place_json['value'] = pl.name
#     results.append(place_json)

class GetNodesData(APIView):
    def get(self, request):
        fetch_info = {
            'node_type': request.GET.get('t', 'Country'),
            'name': request.GET.get('q', ''),
            'limit': 10,
            'page': int(request.GET.get('p', 1)),
        }

        print("akjfkaf" + fetch_info['node_type'] + " node " + fetch_info['name'])
        nodes = fetch_nodes(fetch_info)
        data = {
            'response': {
                'status': '200',
                'rows': len(nodes),
                'data': nodes,
            },
        }
        return Response(data)


class GetCountries(APIView):
    def get(self, request):
        countries = fetch_countries()
        data = {
            'response': {
                'status': '200',
                'data': countries,
            },
        }
        return Response(data)


def _get_node_properties(node):
    """Get the properties from a neo4j.v1.types.graph.Node object."""
    # 1.6.x and newer have it as `_properties`
    if hasattr(node, '_properties'):
        return node._properties
    # 1.5.x and older have it as `properties`
    else:
        return node.properties
