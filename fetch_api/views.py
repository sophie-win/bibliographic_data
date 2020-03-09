import json

import neo4j
from django.http import HttpResponse
from django.shortcuts import render
from neomodel import Q

from . import my_dict
from .models import Country
from .positional_intersect import run_test
from .skip_pointer import intersection_with_skips
from .utils import (fetch_nodes, fetch_countries, filter_countries, json_api_call, book_and_author)

from rest_framework.views import APIView
from rest_framework.response import Response
import json


def get_suggestions(request):
    # first_posting_list = [1,2,3,4,8,16,19,23,28,43,88,99,120,135]
    # second_posting_list = [1, 2, 3,4, 5, 8, 41, 51, 60, 71, 88,99,100,101,102,103,104,105,135,140,155,160]
    # print('list created')
    # result = intersection_with_skips(first_posting_list, second_posting_list)
    # mylist = ["hello", "world"]
    # print('my first ', first_posting_list[0])
    # print(result)
    # run_test()
    # print(a[1] + ' a')
    # print(result)
    print("hey")
    if request.is_ajax():
        term = request.GET.get('term', '')
        # get_list(request, term)
        places = filter_countries(term)
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
                print('node 0', type(node[0][0]))
                for l in labels:
                    node_type = l
                    print(node_type)

                node_properties = _get_node_properties(node[0][0])
                # if node_properties[node_type]
                found_property = node[0][1]
                print(node_properties[found_property] + " node")
                if node_type == 'Book':
                    if found_property != 'name':
                        data_value = node_properties[found_property] + ', ' + node_properties['name']
                    else:
                        data_value = node_properties['name']
                    place_json = {'value': data_value, 'node_type': node_type, 'name': node_properties['name']}
                    results.append(place_json)
                for keyValue in node_properties:
                    # print(node_properties[keyValue])

                    place_json = {'value': node_properties[keyValue]}
                    # if q in node_properties[keyValue]:
                    #     if not results.__contains__(place_json):
                    # results.append(place_json)

        data = json.dumps(results)
        print('type_d', type(data))
    else:
        print("fail")
        data = 'fail'

    mime_type = 'application/json'
    return HttpResponse(data, mime_type)


def get_json_data(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # print('list_hey')
    # print("get_list")
    if request.is_ajax():

        print("ajax correct")
        query_str = request.GET.get('term', '')
        # print("term is " + q)
        datas = json_api_call(query_str)

        # print('j_term', query_str)
        # print('type hey', datas)
        results = []
        # print('length', len(datas))

        for data in datas:
            for r in data:
                # print('printloop', type(r), r)

                j_data = json.loads(r)
                # print('data_type', type(j_data))
                nodes = j_data['nodes']
                # print('hey', type(nodes))
                del j_data['nodes']
                # print('j', str(j_data))
                new_nodes_list = []
                for n in nodes:
                    node = {"id": n["id"], "labels": n["labels"]}
                    properties = {}
                    # print('s', str(node))
                    for key in n:
                        if key != 'label' and key != 'id':
                            # properties += key + ":" + n[key] + ","
                            properties[key] = n[key]
                    node["properties"] = properties

                    new_nodes_list.append(node)
                    # print(type(node))
                j_data["nodes"] = new_nodes_list
                # h_d = json.loads(str(j_data))
                # print('ty', str(h_d) )
        required_data_data = {'data': [{'graph': j_data}]}
        required_data = {'results': [required_data_data]}
        # print('h', j_data)
        my_data = json.dumps(required_data)
        # print('d')

    else:
        print("fail")
        data = 'fail'
    mime_type = 'application/json'
    f = open("templates/json/dd.json", "w")
    f.write(my_data)
    f.close()
    # print(my_dict(my_data))
    # print(HttpResponse(data, mime_type).getvalue())
    return HttpResponse(my_data, mime_type)


def get_list(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    print('list_hey')
    print("get_list")
    if request.is_ajax():

        print("ajax correct")
        query_str = request.GET.get('term', '')
        # print("term is " + q)
        datas = book_and_author(query_str)
        # print('type', type(datas))
        print("lent db ", datas)
        results = []
        print('length', len(datas))
        for data in datas:
            print('printloop', len(data[0]))
            d = data[0]
            for a in d:
                # node_obj = neo4j.types.graph.Node(a)
                # print('a', type(node_obj))
                print(d[a])
            if isinstance(data[0], int):
                print("here")
            else:
                # labels = node[0].labels
                # for l in labels:
                #     node_type = l
                #     print(node_type)

                node_properties = _get_node_properties(data[0])
                attributes = ''
                for keyValue in node_properties:
                    attributes = node_properties[keyValue]
                print(attributes)
                place_json = {'value': attributes}
                results.append(place_json)
        data = json.dumps(results)
    else:
        print("fail")
        data = 'fail'

    for r in results:
        print('final', r)
    mime_type = 'application/json'
    return HttpResponse(data, mime_type)

    # results = []
    #
    # for node in places:
    #     # print(node[0])
    #     # place_json['label'] = node.name
    #     # place_json['value'] = pl.name
    #     if isinstance(node[0], int):
    #         print("here")
    #     else:
    #         node_properties = _get_node_properties(node[0])
    #         for keyValue in node_properties:
    #             # print(node_properties[keyValue])
    #             place_json = {'value': node_properties[keyValue]}
    #             # if q in node_properties[keyValue]:
    #             #     if not results.__contains__(place_json):
    #         results.append(node_properties)
    #         print(results)
    #         context = {'results': results}
    # return render(request, 'detail.html', context)


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
