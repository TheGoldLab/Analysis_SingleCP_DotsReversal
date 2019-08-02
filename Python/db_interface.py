"""
This module sets up the db as described here:
https://adrianblogtech.wordpress.com/2018/10/24/plan-for-a-new-code-management-app/
"""
from contextlib import contextmanager
import pyArango.connection as pyconn
from pyArango.document import Document
import pyArango.collection as pcl
from pyArango.graph import Graph, EdgeDefinition
import pyArango.validation as pvl
from pyArango.theExceptions import ValidationError, InvalidDocument
import json
import os
import pprint

PATH_TO_CONFIG = os.path.expanduser('~/.iksci')


DB_NAMES = {
    'collections_descriptions': {
        'projects': 'global research project/topic',
        'subproject_links': 'everything in the subproject also belongs to the parent project',
        'files': 'files objects (can reside in a remote location)',
        'code': 'code (tracked with Git)',
        'code_params': 'parameter values used by code',
        'documents': 'general research documents',
        'figures': 'info about figures',
        'data': 'info about data',
        'code_to_code': 'the target code requires the source code to execute properly',
        'code_to_doc': 'the document mentions the code',
        'code_to_fig': 'producing the figure requires the code -see blog for ambiguity resolution',
        'params_to_code': 'the code was run with these parameter inputs',
        'code_to_data': 'code is required to produce the data -see blog for ambiguity resolution',
        'data_to_code': 'the code makes use of the data to run properly',
        'fig_to_doc': 'document uses or mentions a figure',
        'doc_to_doc': 'target doc mentions source doc',
        'data_to_doc': 'document mentions/explains the data',
        'file_to_code': 'code lives in file',
        'file_to_doc': 'doc lives in file',
        'file_to_fig': 'fig lives in file',
        'file_to_data': 'data lives in file',
    },
    'collections': {
        'projects': 'Projects',
        'subproject_links': 'SubprojectRelation',
        'files': 'File',
        'code': 'Code',
        'code_params': 'CodeParams',
        'documents': 'Documents',
        'figures': 'Figs',
        'data': 'Data',
        'code_to_code': 'CodeToCode',
        'code_to_doc': 'CodeToDoc',
        'code_to_fig': 'CodeToFig',
        'params_to_code': 'ParamsToCode',
        'code_to_data': 'CodeToData',
        'data_to_code': 'DataToCode',
        'fig_to_doc': 'FigToDoc',
        'doc_to_doc': 'DocToDoc',
        'data_to_doc': 'DataToDoc',
        'file_to_code': 'FileToCode',
        'file_to_doc': 'FileToDoc',
        'file_to_fig': 'FileToFig',
        'file_to_data': 'FileToData',
    },
    'graphs': {
        'all_projects': 'ProjectsGraph',
        'everything': 'TheGraphWithEverything',
    },
    'fields': {
        'projects': ['name', 'description'],
        'subproject_links': [],
        'files': ['url', 'path', 'filename', 'checksum', 'format'],
        'code': ['url', 'repo', 'commit'],
        'code_params': [],
        'documents': ['title', 'description'],
        'figures': ['title', 'description'],
        'data': [],
        'code_to_code': [],
        'code_to_doc': [],
        'code_to_fig': [],
        'params_to_code': [],
        'code_to_data': [],
        'data_to_code': [],
        'fig_to_doc': [],
        'doc_to_doc': [],
        'data_to_doc': [],
        'file_to_code': [],
        'file_to_doc': [],
        'file_to_fig': [],
        'file_to_data': [],
    }
}
assert len(DB_NAMES['fields']) == len(DB_NAMES['collections'])


def list_coll_names(as_in_arangodb=False):
    """
    list all collection names
    :param as_in_arangodb: (bool) if True, shows names of collections in arangodb database
    :return: None but calls pprint.pprint
    """
    if as_in_arangodb:
        pprint.pprint(list(DB_NAMES['collections'].values()))
    else:
        pprint.pprint(list(DB_NAMES['collections'].keys()))


def list_fields(coll):
    assert coll in DB_NAMES['collections'].keys(), 'invalid collection name'
    pprint.pprint(DB_NAMES['fields'][coll])


@contextmanager
def session(config='default', create_if_missing=False, verbose=True):
    """
    The aim of this context manager (meant to be used in a with statement) is to:
        1. connect to ArangoDB with credentials fetched from a .json config file
        2. check whether the database is properly configured for indiek
    todo: accept on-the-fly configuration (no need to read from config file)
    """
    with open(PATH_TO_CONFIG) as f:
        conf = json.load(f)[config + '_config']

    conn = pyconn.Connection(username=conf['username'], password=conf['password'], arangoURL=conf['url'])
    db_name = conf['database']

    if not conn.hasDatabase(db_name):
        raise LookupError(f"database {db_name} not found; either it doesn't exist or arangodb"
                          f" user {conf['username']} from your config file doesn't have proper permissions")

    db = conn[db_name]

    def check_db_infrastructure(create_missing):
        """
        todo: provide option to delete useless collections (and graphs?)
        :param create_missing: (bool) if True, creates required collections and graphs for IndieK
        :return: None
        """

        def check_coll(coll, cls):
            """
            :param coll: (str) name of collection
            :param cls: (str) name of collection's class
            :return:
            """
            if not db.hasCollection(coll):
                if verbose:
                    print(f"collection {coll} not found in db {db.name}")
                if create_missing:
                    db.createCollection(name=coll, className=cls)
                    if verbose:
                        print(f"collection {coll} created")

        coll_names = list(DB_NAMES['collections'].values())
        coll_classes = coll_names

        for coll_name, coll_cls in zip(coll_names, coll_classes):
            check_coll(coll_name, coll_cls)

        graph_names = list(DB_NAMES['graphs'].values())
        for graph_name in graph_names:
            if not db.hasGraph(graph_name):
                if verbose:
                    print(f"database {db.name} has no graph named {graph_name}")
                if create_missing:
                    db.createGraph(graph_name, createCollections=False)
                    if verbose:
                        print(f"graph {graph_name} created")

    check_db_infrastructure(create_if_missing)

    try:
        yield db
    finally:
        conn.disconnectSession()


def db_setup(config_str, verbose=True):
    """
    Convenience function to make sure the database corresponding to the passed configuration string is set up.
    :param config_str: should match the config name in the config file (PATH_TO_CONFIG), e.g. 'default', 'test_db', etc.
    :param verbose: (bool) passed to session()
    :return: None
    """
    with session(config=config_str, create_if_missing=True, verbose=verbose):
        pass


def db_erase(config_str):
    """
    erases (drops) collections and graphs corresponding to indiek in the database mentioned in config_str
    :param config_str: should match the config name in the config file (PATH_TO_CONFIG), e.g. 'default', 'test_db', etc.
    :return:
    """
    with session(config=config_str, create_if_missing=False) as db:
        db.dropAllCollections()


def equal_docs(d1, d2):
    return [d1[k] for k in d1.privates] == [d2[k] for k in d2.privates]


def extract_doc_privates(d):
    return tuple([d[k] for k in d.privates])


def get_project_by_name(database, project_name, as_simple_query=False):
    """
    fetches project if exists, returns None otherwise
    todo: figure out what batchSize does
    Args:
        database: DBHandle or Database from pyArango module
        project_name: string, name of project
        as_simple_query: bool, if true returns SimpleQuery object, if false (default) returns Document object
    Returns:
        pyArango.query.SimpleQuery OR Projects document
    """
    project_coll = DB_NAMES['collections']['projects']
    name_field = 'name'
    assert name_field in DB_NAMES['fields']['projects']
    simple_query = database[project_coll].fetchByExample({name_field: project_name}, batchSize=100)
    if as_simple_query:
        return simple_query
    if simple_query.count > 0:
        return simple_query[0]
    else:
        return None


def get_relation_name(source_doc, target_doc):
    """
    finds the appropriate relation name for two documents to link
    :param source_doc: pyArango doc
    :param target_doc: pyArango doc
    :return: appropriate edge collection name
    """
    source_coll = source_doc.collection.name
    target_coll = target_doc.collection.name

    def coll2tag(coll):
        mapping = {
            'files': 'file',
            'code': 'code',
            'code_params': 'params',
            'documents': 'doc',
            'figures': 'fig',
            'data': 'data,'
        }
        for k, v in DB_NAMES['collections'].items():
            if coll == v:
                return mapping[k]

    coll_key = coll2tag(source_coll) + '_to_' + coll2tag(target_coll)

    return DB_NAMES['collections'][coll_key]


def display(elements, title, separator='==========', hide_privates=True, only_fields=None):
    """
    todo: accept graph-like argument
    todo: accept optional argument to only display specific fields
    todo: control field order in display
    :param elements: iterable of pyarango docs, (e.g. simple query object)
    :param title: str to display before anything else
    :param separator: str to display in between elements
    :param hide_privates: bool. If True, private doc attributes not shown. But interaction with only_fields arg are
                          complex, read below
    :param only_fields: list of strings containing field names for document store.
                        case1: only_fields is None; then hide_privates has highest authority
                        case2: only_fields is not None and only_fields contains no private field; then, all fields in
                          only_fields are displayed, and private fields are displayed according to hide_privates value
                        case3: only_fields contains a private field and hide_privates is False, then all private fields
                          are displayed, as well as the non-private fields from only_fields
                        case4: only_fields contains a private field and hide_privates is True, then only the fields in
                          only_fields are displayed.
    :return:
    """
    print(title)
    for el in elements:
        def delete_field(key):
            """
            :param key: key from store
            :return: True if key-value pair should be deleted from store
            """
            # two conditions in which field should be deleted, in most cases
            hide_privates_cond = hide_privates and (key in el.privates)
            only_fields_cond = (only_fields is not None) and (key not in only_fields)

            if only_fields is None:
                return hide_privates_cond  # case 1
            if only_fields is not None:
                assert len(set(only_fields)) == len(only_fields), "duplicate fields in argument only_fields"
                # bool below is True if only_fields contains no private field
                null_intersection = not bool(set(only_fields).intersection(set(el.privates)))
                if null_intersection:  # case 2
                    if hide_privates_cond or only_fields_cond:
                        return True
                    return False
                if hide_privates:
                    return only_fields_cond  # case 4
                return key not in set(only_fields).union(set(el.privates))  # case 3

        content = el.getStore()

        for k, v in content.items():
            if not delete_field(k):
                try:
                    print(k + ': ' + v)
                except TypeError:
                    print(k + ': ', v)
        print(separator)


class Projects(pcl.Collection):
    """
    Document collection for pyArango corresponding to projects
    """
    # not convinced the _properties below are all necessary
    _properties = {
        "keyOptions": {
            "allowUserKeys": False,
            "type": "autoincrement",
        }
    }

    _validation = {
        'on_save': False,
        'on_set': False,
        'allow_foreign_fields': True  # allow fields that are not part of the schema
    }


class SubprojectRelation(pcl.Edges):
    """edge class to use to assign a project as a subproject of another"""
    pass


class ProjectsGraph(Graph):
    """graph of all projects in the database. All project management occurs through this graph."""
    _edgeDefinitions = [EdgeDefinition("SubprojectRelation",
                                       fromCollections=[DB_NAMES['collections']['projects']],
                                       toCollections=[DB_NAMES['collections']['projects']])]
    _orphanedCollections = []


class CodeToCode(pcl.Edges):
    pass


class CodeToDoc(pcl.Edges):
    pass


class CodeToFig(pcl.Edges):
    pass


class ParamsToCode(pcl.Edges):
    pass


class CodeToData(pcl.Edges):
    pass


class DataToCode(pcl.Edges):
    pass


class FigToDoc(pcl.Edges):
    pass


class DocToDoc(pcl.Edges):
    pass


class DataToDoc(pcl.Edges):
    pass


class FileToDoc(pcl.Edges):
    pass


class FileToCode(pcl.Edges):
    pass


class FileToFig(pcl.Edges):
    pass


class FileToData(pcl.Edges):
    pass


class TheGraphWithEverything(Graph):
    _edgeDefinitions = [
        EdgeDefinition(DB_NAMES['collections']['code_to_code'],
                       fromCollections=[DB_NAMES['collections']['code']],
                       toCollections=[DB_NAMES['collections']['code']]),
        EdgeDefinition(DB_NAMES['collections']['code_to_doc'],
                       fromCollections=[DB_NAMES['collections']['code']],
                       toCollections=[DB_NAMES['collections']['documents']]),
        EdgeDefinition(DB_NAMES['collections']['code_to_fig'],
                       fromCollections=[DB_NAMES['collections']['code']],
                       toCollections=[DB_NAMES['collections']['figures']]),
        EdgeDefinition(DB_NAMES['collections']['params_to_code'],
                       fromCollections=[DB_NAMES['collections']['code_params']],
                       toCollections=[DB_NAMES['collections']['code']]),
        EdgeDefinition(DB_NAMES['collections']['code_to_data'],
                       fromCollections=[DB_NAMES['collections']['code']],
                       toCollections=[DB_NAMES['collections']['data']]),
        EdgeDefinition(DB_NAMES['collections']['data_to_code'],
                       fromCollections=[DB_NAMES['collections']['data']],
                       toCollections=[DB_NAMES['collections']['code']]),
        EdgeDefinition(DB_NAMES['collections']['fig_to_doc'],
                       fromCollections=[DB_NAMES['collections']['figures']],
                       toCollections=[DB_NAMES['collections']['documents']]),
        EdgeDefinition(DB_NAMES['collections']['doc_to_doc'],
                       fromCollections=[DB_NAMES['collections']['documents']],
                       toCollections=[DB_NAMES['collections']['documents']]),
        EdgeDefinition(DB_NAMES['collections']['data_to_doc'],
                       fromCollections=[DB_NAMES['collections']['data']],
                       toCollections=[DB_NAMES['collections']['documents']]),
        EdgeDefinition(DB_NAMES['collections']['file_to_doc'],
                       fromCollections=[DB_NAMES['collections']['files']],
                       toCollections=[DB_NAMES['collections']['documents']]),
        EdgeDefinition(DB_NAMES['collections']['file_to_code'],
                       fromCollections=[DB_NAMES['collections']['files']],
                       toCollections=[DB_NAMES['collections']['code']]),
        EdgeDefinition(DB_NAMES['collections']['file_to_fig'],
                       fromCollections=[DB_NAMES['collections']['files']],
                       toCollections=[DB_NAMES['collections']['figures']]),
        EdgeDefinition(DB_NAMES['collections']['file_to_data'],
                       fromCollections=[DB_NAMES['collections']['files']],
                       toCollections=[DB_NAMES['collections']['data']]),
    ]
    _orphanedCollections = []


class Data(pcl.Collection):
    _properties = {
        "keyOptions": {
            "allowUserKeys": False,
            "type": "autoincrement",
        }
    }


class Code(pcl.Collection):
    _properties = {
        "keyOptions": {
            "allowUserKeys": False,
            "type": "autoincrement",
        }
    }


class Documents(pcl.Collection):
    _properties = {
        "keyOptions": {
            "allowUserKeys": False,
            "type": "autoincrement",
        }
    }


class UserInterface:
    """
    Class through which all user interactions with ik database occurs. Should be used within a with block that provides
    the database as a context, via the session() module function.
    """
    def __init__(self, db):
        self.db = db
        self.projects_graph = self.db.graphs[DB_NAMES['graphs']['all_projects']]
        self.everything = self.db.graphs[DB_NAMES['graphs']['everything']]

    """--------------projects methods-------------"""

    def create_project(self, name, descr):
        """
        :param name: project name (see Projects._fields for constraints)
        :param descr: project description (see Projects._fields for constraints)
        :return: document if project successfully created, otherwise None
        """
        if get_project_by_name(self.db, name, as_simple_query=True):
            print(f"project '{name}' already exists")
            doc = None
        else:
            doc = self.projects_graph.createVertex(
                DB_NAMES['collections']['projects'],
                {
                    'name': name,
                    'description': descr,
                }
            )
            doc.save()
            # todo: add vertex to project_to_expt_graph as well?
        return doc

    def delete_project(self, doc):
        """remove project from database, and all linked edges"""
        self.projects_graph.deleteVertex(doc)
        # todo: remove vertex from project_to_expt_graph as well?

    def list_projects(self):
        """
        lists all projects in database
        :return:
        """

        simple_query = self.db[DB_NAMES['collections']['projects']].fetchAll()

        display(simple_query, title=f'LIST OF {simple_query.count} TOPICS IN DB')

    def set_subproject(self, supraproject, subproject):
        """
        sets project "subproject" as subproject of "supraproject"
        :param supraproject: project document or project name
        :param subproject: project document or project name
        :return:

        todo: check that project1 and project2 are 'up-to-date' before saving the link
        todo: get genealogy of both projects and warn the user if genalogies have non-zero intersection
        """
        name_field = 'name'
        subname = subproject if isinstance(subproject, str) else subproject[name_field]
        supname = supraproject if isinstance(supraproject, str) else supraproject[name_field]
        if self.has_as_descendent(supraproject, subproject):
            print(f"project {subname} is already a descendent "
                  f"of project {supname}. No new link created.")
        elif self.has_as_descendent(subproject, supraproject):
            print(f"project {subname} is already an ancestor "
                  f"of project {supname}. No new link created to avoid loop.")
        else:
            if isinstance(supraproject, str):
                supraproject = get_project_by_name(self.db, supraproject)
            if isinstance(subproject, str):
                subproject = get_project_by_name(self.db, subproject)
            self.projects_graph.link('SubprojectRelation', supraproject, subproject, {})

    def has_as_descendent(self, supra, sub):
        """
        True if sub is in the list of subproject descendents of supra
        :param supra: project document (or name as str) supposed to be ancestor
        :param sub: project document (or name as str) supposed to be descendent
        :return: (bool)
        """
        if isinstance(supra, str):
            supra = get_project_by_name(self.db, supra)

        list_of_descendents = self.get_connected_component(supra, direction='outbound')

        if isinstance(sub, str):
            to_return = sub in list_of_descendents
        else:
            n = 'name'
            to_return = sub[n] in list_of_descendents
        return to_return

    def clear_projects(self):
        """
        removes all projects and their associated subproject links from database.
        Doesn't delete collections
        :return:
        """
        simple_query = self.db[DB_NAMES['collections']['projects']].fetchAll()

        for project in simple_query:
            self.projects_graph.deleteVertex(project)

    def get_connected_component(self, project, direction='outbound', depth=None):
        """
        my idea for this method is to create a graph in the database that corresponds to all the genealogy
        (ancestors and descendents) of a project
        :param project: any project document
        :param direction:
        :param depth:
        :return: a list of vertices

        todo: control for duplicates in returned list?
        """
        name_field = 'name'
        if depth is None:
            q = self.projects_graph.traverse(project, direction=direction)

            return [d[name_field] for d in q['visited']['vertices']]
        else:
            graph_name = DB_NAMES['graphs']['all_projects']

            q_str = f"FOR v IN 0..{depth} {direction.upper()} '{project._id}' " \
                    f"GRAPH '{graph_name}' " \
                    f"RETURN v.{name_field}"
            return self.db.AQLQuery(q_str, rawResults=True)

    def get_extremal_projects(self, kind='minimal'):
        simple_query = self.db[DB_NAMES['collections']['projects']].fetchAll()

        if kind == 'minimal':
            dirr = 'inbound'
        elif kind == 'maximal':
            dirr = 'outbound'
        elif kind == 'singleton':
            dirr = 'any'
        else:
            raise ValueError("Invalid 'kind' argument, expects 'minimal', 'maximal' or 'singleton'")

        project_list = []
        for t in simple_query:
            if len(self.get_connected_component(t, direction=dirr, depth=1)) == 1:
                project_list.append(t)

        return project_list

    def import_projects(self, f):
        """
        :param f: file-like object with read permission
        :return:
        """
        data = json.load(f)
        exclude = []
        for t in data['projects']:
            try:
                self.create_project(t['name'], t['description'])
            except InvalidDocument as err:
                exclude.append(t['name'])
                print(f"Can't import project with name {t['name']}")
                print(err)
        for r in data['relations']:
            if r['supraproject'] not in exclude and r['subproject'] not in exclude:
                self.set_subproject(r['supraproject'], r['subproject'])

    """------------other methods--------------"""

    def create_item(self, coll, content):
        """
        create a general item (any collection except a project)
        :param coll: (str) collection name, must be a key of DB_NAMES['collections']
        :param content: (dict) key-values for docunent's Store
        :return: document if experiment successfully created, otherwise None
        """
        assert coll in DB_NAMES['collections'].keys()
        assert coll != DB_NAMES['collections']['projects'], 'use create_project to create a project'

        doc = self.everything.createVertex(
            DB_NAMES['collections'][coll],
            content
        )
        doc.save()
        return doc

    def delete_item(self, doc):
        """remove item from database, and all linked edges. To remove a project, use delete_project"""
        # todo: check that doc is NOT a project
        self.everything.deleteVertex(doc)

    def list_items(self, coll):
        """
        :return:
        """
        assert coll in DB_NAMES['collections'].keys()
        assert coll != DB_NAMES['collections']['projects'], 'use list_projects to list projects'

        simple_query = self.db[DB_NAMES['collections'][coll]].fetchAll()

        display(simple_query, title=f'LIST OF {simple_query.count} EXPERIMENTS IN DB')

    def set_link(self, source_doc, target_doc):
        self.everything.link(get_relation_name(source_doc, target_doc), source_doc, target_doc, {})


# def doc_in_list(document, list_of_docs):
#     doc_id = document['_id']
#     id_list = [d['_id'] for d in list_of_docs]
#     return doc_id in id_list
#
#
# def subproject_link_exists(db, project1, project2):
#     out_edges = db[COLL_NAMES['subproject_links']].getOutEdges(project1)
#     in_edges = db[COLL_NAMES['subproject_links']].getInEdges(project2)
#     return any([doc_in_list(o, in_edges) for o in out_edges])
#
#
# def create_subproject_link(db, project1, project2):
#     """

#     :param db:
#     :param project1: project obj
#     :param project2: project obj
#     :return:
#     """
#     if subproject_link_exists(db, project1, project2):
#         print('subproject link exists, link creation aborted')
#         return None
#
#     link = db[COLL_NAMES['subproject_links']].createEdge()
#     link['_from'] = project1['_id']
#     link['_to'] = project2['_id']
#
#     link.save()
#     return link


if __name__ == "__main__":
    pass
