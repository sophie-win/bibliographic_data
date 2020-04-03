import json
import re

import neo4j
from django.http import HttpResponse
from django.shortcuts import render
from neomodel import Q

from .utils import (fetch_nodes, fetch_countries, filter_countries, json_api_call, book_and_author,
                    family_tree_json_api_call, family_tree_normal, family_tree_child, sample_data,
                    get_nodes_and_relationships)

from rest_framework.views import APIView
from rest_framework.response import Response
import json
import yaml

def get_suggestions(request):
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
                print(node_properties[found_property] + " node", found_property)
                # if node_type == 'Book':
                if found_property != 'name':
                    print('name')
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

    if request.is_ajax():
        query_str = request.GET.get('term', '')
        query_data = re.sub(r"'", "\\'", query_str)

        datas = json_api_call(query_data)

        for data in datas:
            for r in data:
                # print('printloop', type(r), r)
                print(data)
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
                        if key == 'name':
                            # name = n[key].split()[0]
                            # if len(name) < 8:
                            #     name_abbr = name + '\n' + n[key].split()[1]
                            #     print(name_abbr)
                            #
                            # else:
                            name_abbr = n[key][:8] + '..'
                            # print(name_abbr)
                            # print(name_abbr)
                            properties['name_abbr'] = name_abbr
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
        print("ajax correct")
        query_str = request.GET.get('term', '')
        # print("term is " + q)
        query_data = re.sub(r"'", "\\'", query_str)

        datas = json_api_call(query_data)

        # print('j_term', query_str)
        # print('type hey', datas)
        results = []
        # print('length', len(datas))

        for data in datas:
            for r in data:
                # print('printloop', type(r), r)
                print(data)
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
                        if key == 'name':
                            # name = n[key].split()[0]
                            # if len(name) < 8:
                            #     name_abbr = name + '\n' + n[key].split()[1]
                            #     print(name_abbr)
                            #
                            # else:
                            name_abbr = n[key][:8] + '..'
                            # print(name_abbr)
                            # print(name_abbr)
                            properties['name_abbr'] = name_abbr
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
    mime_type = 'application/json'
    f = open("templates/json/dd.json", "w")
    f.write(my_data)
    f.close()
    # print(my_dict(my_data))
    # print(HttpResponse(data, mime_type).getvalue())
    return HttpResponse(my_data, mime_type)

def get_node_relationships(request):

    if request.is_ajax():
        query_str = request.GET.get('node_id', '')

        datas = get_nodes_and_relationships(query_str)

        for data in datas:
            for r in data:
                # print('printloop', type(r), r)
                print(data)
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
                        if key == 'name':
                            # name = n[key].split()[0]
                            # if len(name) < 8:
                            #     name_abbr = name + '\n' + n[key].split()[1]
                            #     print(name_abbr)
                            #
                            # else:
                            name_abbr = n[key][:8] + '..'
                            # print(name_abbr)
                            # print(name_abbr)
                            properties['name_abbr'] = name_abbr
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
        print("ajax correct")
        query_str = request.GET.get('term', '')
        # print("term is " + q)
        query_data = re.sub(r"'", "\\'", query_str)

        datas = json_api_call(query_data)

        # print('j_term', query_str)
        # print('type hey', datas)
        results = []
        # print('length', len(datas))

        for data in datas:
            for r in data:
                # print('printloop', type(r), r)
                print(data)
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
                        if key == 'name':
                            # name = n[key].split()[0]
                            # if len(name) < 8:
                            #     name_abbr = name + '\n' + n[key].split()[1]
                            #     print(name_abbr)
                            #
                            # else:
                            name_abbr = n[key][:8] + '..'
                            # print(name_abbr)
                            # print(name_abbr)
                            properties['name_abbr'] = name_abbr
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
    mime_type = 'application/json'
    f = open("templates/json/dd.json", "w")
    f.write(my_data)
    f.close()
    # print(my_dict(my_data))
    # print(HttpResponse(data, mime_type).getvalue())
    return HttpResponse(my_data, mime_type)

def data_loop(sec_gen, input_children):
    child = input_children
    for data in sec_gen:
        if isinstance(data[0], int):
            print("here")
        else:
            start_node = _get_node_properties(data[0])
            print(start_node)
            rs = _get_node_properties(data[1])
            end_node = _get_node_properties(data[2])
            print(rs['name'])
            if rs['name'] == 'mother':
                if 'children' in child:
                    child['children'].append(end_node)
                else:
                    child['children'] = [end_node]

                # print(child['children'], 'ch')
            elif rs['name'] == 'husband' or rs['name'] == 'wife' or rs['name'] == 'first_wife':
                # print('hs')
                print(end_node['id'], start_node['id'])
                if end_node['id'] != child['id']:
                    print('not equal')
                    if 'spouse' not in child:
                        print('sp in child already')
                    #     child['spouse'].append(end_node)
                    # else:
                    #     print('el', child)
                        child['spouse'] = end_node
                        print(child['spouse'])
                # print(type(child['spouse']))

    return child


def get_family_tree(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # print('list_hey')
    print("get_list")
    if request.is_ajax():

        print("ajax correct")
        query_str = request.GET.get('term', '')
        # print("term is " + q)
        query_data = re.sub(r"'", "\\'", query_str)

        datas = family_tree_child(query_data)
        results = []
        print('length', len(datas))
        my_resuts = {}
        for data in datas:
            if isinstance(data[0], int):
                print("here")
            else:

                start_node = _get_node_properties(data[0])
                my_resuts = start_node
        for node in datas:
            if isinstance(node[0], int):
                print("here")
            else:
                print('hey see')
                # for type of the node
                # print(start_node)

                rs = _get_node_properties(node[1])
                end_node = _get_node_properties(node[2])
                print('endNode', end_node)
                if rs['name'] == 'father' or rs['name'] == 'mother':
                    if 'children' in my_resuts:
                        my_resuts['children'].append(end_node)
                    else:
                        my_resuts['children'] = [end_node]
                    # my_resuts['id'] = start_node['id']
                    # my_resuts['children'] = [{'id': end_node['id']}]
                    children = my_resuts['children']
                    r_children = children
                    child_order = 0
                    print('s', len(r_children))
                    for child in r_children:
                        sec_gen = family_tree_normal(child['name'])
                        # print(len(sec_gen))
                        if len(sec_gen) != 0:
                            second_child = data_loop(sec_gen, child)
                            my_resuts['children'][child_order] = second_child
                            # print(len(second_child['children']))
                            sec_child_order = 0
                            if 'children' in second_child:
                                for sec_child in second_child['children']:
                                    third_gen = family_tree_normal(sec_child['name'])
                                    if len(third_gen) != 0:
                                        third_children = data_loop(third_gen, sec_child)
                                        my_resuts['children'][child_order]['children'][sec_child_order] = third_children
                                        third_child_order = 0
                                        if 'children' in third_children:
                                            for third_child in third_children['children']:
                                                forth_gen = family_tree_normal(third_child['name'])
                                                if len(forth_gen) != 0:
                                                    fourth_children = data_loop(forth_gen, third_child)
                                                    my_resuts['children'][child_order]['children'][sec_child_order]['children'][third_child_order] = fourth_children
                                                    fourth_child_order = 0
                                                    if 'children' in fourth_children:
                                                        for forth_child in fourth_children['children']:
                                                            fifth_gen = family_tree_normal(forth_child['name'])
                                                            print('count of ', fourth_child_order)
                                                            if len(fifth_gen) != 0:
                                                                fifth_children = data_loop(fifth_gen, forth_child)
                                                                print('lenof ', len(fifth_children))
                                                                my_resuts['children'][child_order]['children'][sec_child_order][
                                                                    'children'][third_child_order][
                                                                    'children'][fourth_child_order] = fifth_children
                                                                fifth_child_order = 0
                                                                if 'children' in fifth_children:
                                                                    for fifth_child in fifth_children['children']:
                                                                        sixth_gen = family_tree_normal(fifth_child['name'])
                                                                        print('six', fifth_child['name'])
                                                                        if len(sixth_gen) != 0:
                                                                            sixth_children = data_loop(sixth_gen, fifth_child)
                                                                            my_resuts['children'][child_order]['children'][
                                                                                sec_child_order]['children'][third_child_order][
                                                                                'children'][fourth_child_order][
                                                                                'children'][fifth_child_order] = sixth_children
                                                                        fifth_child_order += 1
                                                            fourth_child_order += 1
                                                third_child_order += 1
                                    sec_child_order += 1
                        child_order += 1

        print('r', json.dumps(my_resuts))


    #
    # else:
    #     print("fail")
    #     data = 'fail'
    # print('psl', yml)
    mime_type = 'application/json'
    f = open("templates/json/f_de.yml", "w+")
    json_data = json.loads(json.dumps(my_resuts))
    yaml.dump(json_data, f, allow_unicode=True)

    f.close()
    print('load yaml finished')
    # print(my_dict(my_data))
    # print(HttpResponse(data, mime_type).getvalue())
    return HttpResponse(json_data, mime_type)


def get_family_tree_first_gen(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # print('list_hey')
    # print("get_list")
    if request.is_ajax():

        print("ajax correct")
        query_str = request.GET.get('term', '')
        # print("term is " + q)
        query_data = re.sub(r"'", "\\'", query_str)

        datas = json_api_call(query_data)

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
                        if key == 'name':
                            # name = n[key].split()[0]
                            # if len(name) < 8:
                            #     name_abbr = name + '\n' + n[key].split()[1]
                            #     print(name_abbr)
                            #
                            # else:
                            name_abbr = n[key][:8] + '..'
                            # print(name_abbr)
                            # print(name_abbr)
                            properties['name_abbr'] = name_abbr
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
    # f = open("templates/json/dd.json", "w")
    # f.write(my_data)
    # f.close()
    # print(my_dict(my_data))
    # print(HttpResponse(data, mime_type).getvalue())
    return HttpResponse(my_data, mime_type)

def get_sample_data (request) :
    if request.is_ajax():

        print("ajax correct data sample")
        query_str = request.GET.get('term', '')
        # print("term is " + q)
        datas = sample_data()
        print(datas)
        print(type(datas[0][0]))


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
