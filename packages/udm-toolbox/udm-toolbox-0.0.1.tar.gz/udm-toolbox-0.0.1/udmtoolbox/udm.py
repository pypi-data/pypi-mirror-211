import os
import uuid
import pathlib


def get_swmm_inp_content(filename, flag):
    flag = flag + '\n'
    result = []

    with open(filename, 'r', encoding='utf-8') as f:
        # getting to the flag line
        for line in f:
            if line == flag:
                break
        # adding related lines to results
        for line in f:
            # finish when getting to another section
            if line[0] == '[':
                break
            # skip if this line is blank or annotation
            if line == '\n' or line[0] == ';':
                continue
            result.append(line[0:-1])

    return result


def combine_swmm_inp_contents(content1, content2):
    # generate a name list of content1
    index_dic = []
    for line in content1:
        pair = line.split()
        index_dic.append(pair[0])
    #
    for line in content2:
        pair = line.split()
        index = index_dic.index(pair[0])
        content1[index] = content1[index] + ' ' + ' '.join(pair[1::])
    #
    return content1


def get_swmm_rpt_content(filename, flag):
    # example:
    # res = ut.get_swmm_rpt_content('calculate_temp/test.rpt', 'Node G80F425')
    flag = f'  <<< {flag} >>>\n'
    result = []
    with open(filename, 'r', encoding='utf-8') as f:
        # getting to the flag line
        for line in f:
            if line == flag:
                break
        # adding related lines to results
        i = 0
        for line in f:
            # skip title bar ( four lines )
            if i < 4:
                i = i + 1
                continue
            # finish when getting to another section
            if line == '  \n':
                break
            result.append(line[0:-1])
    return result


class CalculationInformation:
    def __init__(self):
        # general option
        self.flow_unit = 'CFS'
        self.infiltration_method = 'HORTON'
        self.flow_routing_method = 'KINWAVE'
        self.link_offsets_type = 'DEPTH'
        self.force_main_equation = 'H-W'

        self.ignore_rainfall = False
        self.ignore_snow_melt = False
        self.ignore_ground_water = False
        self.ignore_RDII = False
        self.ignore_routing = False
        self.ignore_water_quality = False

        self.allow_ponding = True
        self.skip_steady_state = False
        self.system_flow_tol = 5
        self.lateral_flow_tol = 5

        self.simulation_start = {"year": 2023, "month": 4, "day": 28, "hour": 8, "minute": 0}
        self.simulation_end = {"year": 2023, "month": 4, "day": 28, "hour": 17, "minute": 0}
        self.report_start = {"year": 2023, "month": 4, "day": 28, "hour": 8, "minute": 0}
        self.sweep_start = {"month": 1, "day": 1}
        self.sweep_end = {"month": 12, "day": 31}
        self.dry_days = 0

        self.report_step = {"hour": 0, "minute": 15, "second": 0}
        self.wet_step = {"hour": 0, "minute": 5, "second": 0}  # runoff
        self.dry_step = {"hour": 1, "minute": 0, "second": 0}  # runoff
        self.routing_step = 600  # in seconds
        self.lengthening_step = 0  # in seconds
        self.variable_step = 0
        self.minimum_step = 0.5  # in seconds

        self.inertial_damping = 'PARTIAL'
        self.normal_flow_limited = 'BOTH'

        self.minimum_surface_area = 0
        self.minimum_slope = 0
        self.max_trials = 8
        self.head_tolerance = 0.0015  # in meters

        self.threads = 1
        self.temp_directory = None

        # report section information
        self.report_input = False
        self.report_check_continuity = True
        self.report_flow_statistics = True
        self.report_controls = False
        self.report_subcatchments = 'ALL'
        self.report_nodes = 'ALL'
        self.report_links = 'ALL'

        # map section information
        self.map_dimensions = [0, 0, 1000, 1000]
        self.map_units = 'None'

        # evaporation section information
        self.evaporation_constant = 0
        self.evaporation_dry_only = False

    def write_to_swmm_inp(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('[OPTIONS]\n')
            f.write(f'FLOW_UNITS             {self.flow_unit}\n')
            f.write(f'INFILTRATION           {self.infiltration_method}\n')
            f.write(f'FLOW_ROUTING           {self.flow_routing_method}\n')
            f.write(f'LINK_OFFSETS           {self.link_offsets_type}\n')
            f.write(f'FORCE_MAIN_EQUATION    {self.force_main_equation}\n')
            f.write('\n')
            f.write('IGNORE_RAINFALL        ' + ('YES' if self.ignore_rainfall else 'NO') + '\n')
            f.write('IGNORE_SNOWMELT        ' + ('YES' if self.ignore_snow_melt else 'NO') + '\n')
            f.write('IGNORE_GROUNDWATER     ' + ('YES' if self.ignore_ground_water else 'NO') + '\n')
            f.write('IGNORE_RDII            ' + ('YES' if self.ignore_RDII else 'NO') + '\n')
            f.write('IGNORE_ROUTING         ' + ('YES' if self.ignore_routing else 'NO') + '\n')
            f.write('IGNORE_QUALITY         ' + ('YES' if self.ignore_water_quality else 'NO') + '\n')
            f.write('\n')
            f.write('ALLOW_PONDING          ' + ('YES' if self.allow_ponding else 'NO') + '\n')
            f.write('SKIP_STEADY_STATE      ' + ('YES' if self.skip_steady_state else 'NO') + '\n')
            f.write(f'SYS_FLOW_TOL           {self.system_flow_tol}\n')
            f.write(f'LAT_FLOW_TOL           {self.lateral_flow_tol}\n')

            f.write('\n')
            f.write('START_DATE             ')
            f.write(str(self.simulation_start['month']).zfill(2) + '/')
            f.write(str(self.simulation_start['day']).zfill(2) + '/')
            f.write(str(self.simulation_start['year']) + '\n')
            f.write('START_TIME             ')
            f.write(str(self.simulation_start['hour']).zfill(2) + ':')
            f.write(str(self.simulation_start['minute']).zfill(2) + '\n')
            f.write('END_DATE               ')
            f.write(str(self.simulation_end['month']).zfill(2) + '/')
            f.write(str(self.simulation_end['day']).zfill(2) + '/')
            f.write(str(self.simulation_end['year']) + '\n')
            f.write('END_TIME               ')
            f.write(str(self.simulation_end['hour']).zfill(2) + ':')
            f.write(str(self.simulation_end['minute']).zfill(2) + '\n')
            f.write('REPORT_START_DATE      ')
            f.write(str(self.report_start['month']).zfill(2) + '/')
            f.write(str(self.report_start['day']).zfill(2) + '/')
            f.write(str(self.report_start['year']) + '\n')
            f.write('REPORT_START_TIME      ')
            f.write(str(self.report_start['hour']).zfill(2) + ':')
            f.write(str(self.report_start['minute']).zfill(2) + '\n')
            f.write('SWEEP_START            ')
            f.write(str(self.sweep_start['month']).zfill(2) + '/')
            f.write(str(self.sweep_start['day']).zfill(2) + '\n')
            f.write('SWEEP_END              ')
            f.write(str(self.sweep_end['month']).zfill(2) + '/')
            f.write(str(self.sweep_end['day']).zfill(2) + '\n')

            f.write('\n')
            f.write(f'DRY_DAYS               {self.dry_days}\n')
            f.write('REPORT_STEP            ')
            f.write(str(self.report_step['hour']).zfill(2) + ':')
            f.write(str(self.report_step['minute']).zfill(2) + ':')
            f.write(str(self.report_step['second']).zfill(2) + '\n')
            f.write('WET_STEP               ')
            f.write(str(self.wet_step['hour']).zfill(2) + ':')
            f.write(str(self.wet_step['minute']).zfill(2) + ':')
            f.write(str(self.wet_step['second']).zfill(2) + '\n')
            f.write('DRY_STEP               ')
            f.write(str(self.dry_step['hour']).zfill(2) + ':')
            f.write(str(self.dry_step['minute']).zfill(2) + ':')
            f.write(str(self.dry_step['second']).zfill(2) + '\n')

            f.write('\n')
            f.write(f'ROUTING_STEP           {self.routing_step}\n')
            f.write(f'LENGTHENING_STEP       {self.lengthening_step}\n')
            f.write(f'VARIABLE_STEP          {self.variable_step}\n')
            f.write(f'MINIMUM_STEP           {self.minimum_step}\n')

            f.write('\n')
            f.write(f'INERTIAL_DAMPING       {self.inertial_damping}\n')
            f.write(f'NORMAL_FLOW_LIMITED    {self.normal_flow_limited}\n')
            f.write(f'MIN_SURFAREA           {self.minimum_surface_area}\n')
            f.write(f'MIN_SLOPE              {self.minimum_slope}\n')
            f.write(f'MAX_TRIALS             {self.max_trials}\n')
            f.write(f'HEAD_TOLERANCE         {self.head_tolerance}\n')
            f.write(f'THREADS                {self.threads}\n')
            if self.temp_directory is not None:
                f.write(f'TEMPDIR                {self.temp_directory}\n')

            f.write('\n\n[REPORT]\n')
            f.write('INPUT                  ' + ('YES' if self.report_input else 'NO') + '\n')
            f.write('CONTINUITY             ' + ('YES' if self.report_check_continuity else 'NO') + '\n')
            f.write('FLOWSTATS              ' + ('YES' if self.report_flow_statistics else 'NO') + '\n')
            f.write('CONTROLS               ' + ('YES' if self.report_controls else 'NO') + '\n')
            f.write(f'SUBCATCHMENTS          {self.report_subcatchments}\n')
            f.write(f'NODES                  {self.report_nodes}\n')
            f.write(f'LINKS                  {self.report_links}\n')

            f.write('\n\n[MAP]\n')
            f.write(
                f'DIMENSIONS  {self.map_dimensions[0]}  {self.map_dimensions[1]}  {self.map_dimensions[2]}  {self.map_dimensions[3]}\n')
            f.write(f'Units  {self.map_units}\n')

            f.write('\n\n[EVAPORATION]\n')
            f.write(f'CONSTANT  {self.evaporation_constant}\n')
            f.write('DRY_ONLY  ' + ('YES' if self.evaporation_dry_only else 'NO') + '\n')

    def read_from_swmm_inp(self, filename):
        contents = get_swmm_inp_content(filename, '[OPTIONS]')
        for line in contents:
            pair = line.split()
            match pair[0]:
                case 'FLOW_UNITS':
                    self.flow_unit = pair[1]
                case 'INFILTRATION':
                    self.infiltration_method = pair[1]
                case 'FLOW_ROUTING':
                    self.flow_routing_method = pair[1]
                case 'LINK_OFFSETS':
                    self.link_offsets_type = pair[1]
                case 'FORCE_MAIN_EQUATION':
                    self.force_main_equation = pair[1]
                case 'IGNORE_RAINFALL':
                    self.ignore_rainfall = True if pair[1] == 'YES' else False
                case 'IGNORE_SNOWMELT':
                    self.ignore_snow_melt = True if pair[1] == 'YES' else False
                case 'IGNORE_GROUNDWATER':
                    self.ignore_ground_water = True if pair[1] == 'YES' else False
                case 'IGNORE_RDII':
                    self.ignore_RDII = True if pair[1] == 'YES' else False
                case 'IGNORE_ROUTING':
                    self.ignore_routing = True if pair[1] == 'YES' else False
                case 'IGNORE_QUALITY':
                    self.ignore_water_quality = True if pair[1] == 'YES' else False
                case 'ALLOW_PONDING':
                    self.allow_ponding = True if pair[1] == 'YES' else False
                case 'SKIP_STEADY_STATE':
                    self.skip_steady_state = True if pair[1] == 'YES' else False
                case 'SYS_FLOW_TOL':
                    self.system_flow_tol = int(pair[1])
                case 'LAT_FLOW_TOL':
                    self.lateral_flow_tol = int(pair[1])
                case 'START_DATE':
                    keys = [int(i) for i in pair[1].split('/')]
                    self.simulation_start['year'] = keys[2]
                    self.simulation_start['month'] = keys[0]
                    self.simulation_start['day'] = keys[1]
                case 'START_TIME':
                    keys = [int(i) for i in pair[1].split(':')]
                    self.simulation_start['hour'] = keys[0]
                    self.simulation_start['minute'] = keys[1]
                case 'END_DATE':
                    keys = [int(i) for i in pair[1].split('/')]
                    self.simulation_end['year'] = keys[2]
                    self.simulation_end['month'] = keys[0]
                    self.simulation_end['day'] = keys[1]
                case 'END_TIME':
                    keys = [int(i) for i in pair[1].split(':')]
                    self.simulation_end['hour'] = keys[0]
                    self.simulation_end['minute'] = keys[1]
                case 'REPORT_START_DATE':
                    keys = [int(i) for i in pair[1].split('/')]
                    self.report_start['year'] = keys[2]
                    self.report_start['month'] = keys[0]
                    self.report_start['day'] = keys[1]
                case 'REPORT_START_TIME':
                    keys = [int(i) for i in pair[1].split(':')]
                    self.report_start['hour'] = keys[0]
                    self.report_start['minute'] = keys[1]
                case 'SWEEP_START':
                    keys = [int(i) for i in pair[1].split('/')]
                    self.sweep_start['month'] = keys[0]
                    self.sweep_start['day'] = keys[1]
                case 'SWEEP_END':
                    keys = [int(i) for i in pair[1].split('/')]
                    self.sweep_end['month'] = keys[0]
                    self.sweep_end['day'] = keys[1]
                case 'DRY_DAYS':
                    self.dry_days = int(pair[1])
                case 'REPORT_STEP':
                    keys = [int(i) for i in pair[1].split(':')]
                    self.report_step['hour'] = keys[0]
                    self.report_step['minute'] = keys[1]
                    self.report_step['second'] = keys[2]
                case 'WET_STEP':
                    keys = [int(i) for i in pair[1].split(':')]
                    self.wet_step['hour'] = keys[0]
                    self.wet_step['minute'] = keys[1]
                    self.wet_step['second'] = keys[2]
                case 'DRY_STEP':
                    keys = [int(i) for i in pair[1].split(':')]
                    self.dry_step['hour'] = keys[0]
                    self.dry_step['minute'] = keys[1]
                    self.dry_step['second'] = keys[2]
                case 'ROUTING_STEP':
                    keys = [int(i) for i in pair[1].split(':')]
                    if len(keys) == 1:
                        self.routing_step = keys[0]
                    elif len(keys) == 2:
                        self.routing_step = keys[-1] + keys[-2] * 60
                    elif len(keys) == 3:
                        self.routing_step = keys[-1] + keys[-2] * 60 + keys[-3] * 3600
                    else:
                        pass
                case 'LENGTHENING_STEP':
                    keys = [int(i) for i in pair[1].split(':')]
                    if len(keys) == 1:
                        self.lengthening_step = keys[0]
                    elif len(keys) == 2:
                        self.lengthening_step = keys[-1] + keys[-2] * 60
                    elif len(keys) == 3:
                        self.lengthening_step = keys[-1] + keys[-2] * 60 + keys[-3] * 3600
                    else:
                        pass
                case 'VARIABLE_STEP':
                    self.variable_step = float(pair[1])
                case 'MINIMUM_STEP':
                    self.minimum_step = float(pair[1])
                case 'INERTIAL_DAMPING':
                    self.inertial_damping = pair[1]
                case 'NORMAL_FLOW_LIMITED':
                    self.normal_flow_limited = pair[1]
                case 'MIN_SURFAREA':
                    self.minimum_surface_area = float(pair[1])
                case 'MIN_SLOPE':
                    self.minimum_slope = float(pair[1])
                case 'MAX_TRIALS':
                    self.max_trials = int(pair[1])
                case 'HEAD_TOLERANCE':
                    self.head_tolerance = float(pair[1])
                case 'THREADS':
                    self.threads = int(pair[1])
                case 'TEMPDIR':
                    self.temp_directory = pair[1]
                case _:
                    pass
        contents = get_swmm_inp_content(filename, '[REPORT]')
        for line in contents:
            pair = line.split()
            match pair[0]:
                case 'INPUT':
                    self.report_input = True if pair[1] == 'YES' else False
                case 'CONTINUITY':
                    self.report_check_continuity = True if pair[1] == 'YES' else False
                case 'FLOWSTATS':
                    self.report_flow_statistics = True if pair[1] == 'YES' else False
                case 'CONTROLS':
                    self.report_controls = True if pair[1] == 'YES' else False
                case 'SUBCATCHMENTS':
                    self.report_subcatchments = pair[1]
                case 'NODES':
                    self.report_nodes = pair[1]
                case 'LINKS':
                    self.report_links = pair[1]
        contents = get_swmm_inp_content(filename, '[MAP]')
        for line in contents:
            pair = line.split()
            match pair[0]:
                case 'DIMENSIONS':
                    self.map_dimensions = [float(pair[1]), float(pair[2]), float(pair[3]), float(pair[4])]
                case 'Units':
                    self.map_units = pair[1]
        return 0


class NodeResult:
    def __init__(self):
        self.date = []
        self.time = []  # in minutes
        self.inflow = []
        self.flooding = []
        self.depth = []
        self.head = []


class Node:
    def __init__(self):
        self.name = ''
        self.coordinate = [0.0, 0.0]
        self.elevation = 0
        self.result = NodeResult()

    def read_from_swmm_rpt(self, filename):
        def time_text2minute(text):
            hours, minutes, seconds = text.split(':')
            result = int(minutes) + 60 * int(hours)
            return result

        # clear previous result
        self.result = NodeResult()
        #
        content = get_swmm_rpt_content(filename, f'Node {self.name}')
        for line in content:
            pair = line.split()
            self.result.date.append(pair[0])
            self.result.time.append(time_text2minute(pair[1]))
            self.result.inflow.append(float(pair[2]))
            self.result.flooding.append(float(pair[3]))
            self.result.depth.append(float(pair[4]))
            self.result.head.append(float(pair[5]))


class Junction(Node):
    def __init__(self):
        Node.__init__(self)
        self.maximum_depth = 0
        self.initial_depth = 0
        self.overload_depth = 0
        self.surface_ponding_area = 0
        #
        # dry weather flow
        self.dwf_base_value = 0
        self.dwf_patterns = []


class Outfall(Node):
    def __init__(self):
        Node.__init__(self)
        self.flap_gate = False
        self.route_to = ''


class OutfallFree(Outfall):
    def __init__(self):
        Outfall.__init__(self)


class OutfallNormal(Outfall):
    def __init__(self):
        Outfall.__init__(self)


class OutfallFixed(Outfall):
    def __init__(self):
        Outfall.__init__(self)
        self.stage = 0.0


class OutfallTidal(Outfall):
    def __init__(self):
        Outfall.__init__(self)
        self.tidal = ''


class OutfallTimeseries(Outfall):
    def __init__(self):
        Outfall.__init__(self)
        self.time_series = ''


class NodeList:
    def __init__(self):
        self.node_list = []

    def add_node(self, node_type, node_information):
        def execute(func1, func2):
            def inner():
                # new an object according to node_type
                new_node = func1()
                # add essential information
                if 'name' in node_information:
                    new_node.name = node_information['name']
                else:  # if it can not find name, raise error
                    # print('Unknown Node: Can not recognize node name')
                    return -1
                if 'coordinate' in node_information:
                    new_node.coordinate = node_information['coordinate']
                if 'elevation' in node_information:
                    new_node.elevation = node_information['elevation']
                # for Outfalls
                if 'flap_gate' in node_information:
                    new_node.flap_gate = True if node_information['flap_gate'] == 'YES' else False
                if 'route_to' in node_information:
                    new_node.route_to = node_information['route_to']
                # add node_type related information
                func2(new_node)
                # update node_list
                self.node_list.append(new_node)
                return 0

            return inner

        match node_type:
            case 'junction':
                def junction_type(new_node):
                    if 'maximum_depth' in node_information:
                        new_node.maximum_depth = node_information['maximum_depth']
                    if 'initial_depth' in node_information:
                        new_node.initial_depth = node_information['initial_depth']
                    if 'overload_depth' in node_information:
                        new_node.overload_depth = node_information['overload_depth']
                    if 'surface_ponding_area' in node_information:
                        new_node.surface_ponding_area = node_information['surface_ponding_area']
                    if 'dwf_base_value' in node_information:
                        new_node.dwf_base_value = node_information['dwf_base_value']
                    if 'dwf_patterns' in node_information:
                        new_node.dwf_patterns = node_information['dwf_patterns']

                return execute(Junction, junction_type)()

            case 'outfall_free':
                def outfall_free_type(_):
                    pass

                return execute(OutfallFree, outfall_free_type)()

            case 'outfall_normal':
                def outfall_normal_type(_):
                    pass

                return execute(OutfallNormal, outfall_normal_type)()

            case 'outfall_fixed':
                def outfall_fixed_type(new_node):
                    if 'stage' in node_information:
                        new_node.stage = node_information['stage']

                return execute(OutfallFixed, outfall_fixed_type)()

            case 'outfall_tidal':
                def outfall_tidal_type(new_node):
                    if 'tidal' in node_information:
                        new_node.tidal = node_information['tidal']

                return execute(OutfallTidal, outfall_tidal_type)()

            case 'outfall_time_series':
                def outfall_time_series_type(new_node):
                    if 'time_series' in node_information:
                        new_node.time_series = node_information['time_series']

                return execute(OutfallTimeseries, outfall_time_series_type)()

            case _:
                return -2

    def read_from_swmm_inp(self, filename):
        junction_contents = get_swmm_inp_content(filename, '[JUNCTIONS]')
        coordinates = get_swmm_inp_content(filename, '[COORDINATES]')
        outfall_contents = get_swmm_inp_content(filename, '[OUTFALLS]')
        dwf_contents = get_swmm_inp_content(filename, '[DWF]')

        # coordinate list
        coordinates_dic = {}
        for line in coordinates:
            keys = line.split()
            coordinates_dic[keys[0]] = [float(keys[1]), float(keys[2])]
        # process junctions
        for line in junction_contents:
            pair = line.split()
            dic = {'name': pair[0], 'coordinate': [0.0, 0.0], 'elevation': float(pair[1]),
                   'maximum_depth': float(pair[2]), 'initial_depth': float(pair[3]),
                   'overload_depth': float(pair[4]), 'surface_ponding_area': float(pair[5])}
            dic['coordinate'] = coordinates_dic[dic['name']]
            self.add_node('junction', dic)
        # process outfalls
        for line in outfall_contents:
            pair = line.split()
            dic = {'name': pair[0], 'coordinate': [0.0, 0.0], 'elevation': float(pair[1])}
            dic['coordinate'] = coordinates_dic[dic['name']]
            #
            if pair[-1] == 'YES':
                dic['flap_gate'] = 'YES'
            elif pair[-1] == 'NO':
                dic['flap_gate'] = 'NO'
            else:
                dic['flap_gate'] = pair[-2]
                dic['route_to'] = pair[-1]
            #
            match pair[2]:
                case 'FREE':
                    self.add_node('outfall_free', dic)
                case 'NORMAL':
                    self.add_node('outfall_normal', dic)
                case 'FIXED':
                    dic['stage'] = float(pair[2])
                    self.add_node('outfall_fixed', dic)
                case 'TIDAL':
                    dic['tidal'] = float(pair[2])
                    self.add_node('outfall_tidal', dic)
                case 'TIMESERIES':
                    dic['time_series'] = float(pair[2])
                    self.add_node('outfall_time_series', dic)
                case _:
                    pass
        # process DWF
        for line in dwf_contents:
            pair = line.split()
            for node in self.node_list:
                if node.name == pair[0]:
                    node.dwf_base_value = pair[2]
                    for pattern in pair[3::]:
                        node.dwf_patterns.append(pattern)
        return 0

    def write_to_swmm_inp(self, filename):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write('\n\n[JUNCTIONS]\n')
            f.write(';;Name  Elevation  MaxDepth  InitDepth  SurDepth  Ponding\n')
            for node in self.node_list:
                if isinstance(node, Junction):
                    f.write(
                        f'{node.name:8}  {node.elevation:8.3f}  {node.maximum_depth:8.3f}  {node.initial_depth:8.3f}  {node.overload_depth:8.3f}  {node.surface_ponding_area:8.3f}\n')
            #
            f.write('\n\n[OUTFALLS]\n')
            f.write(';;Name  Elevation  Type  //  Gated  RouteTo\n')
            for node in self.node_list:
                if isinstance(node, OutfallFree):
                    msg = 'YES' if node.flap_gate else 'NO'
                    f.write(f'{node.name:8}  {node.elevation:8.3f}    FREE    {msg:8}  {node.route_to}\n')
                if isinstance(node, OutfallNormal):
                    msg = 'YES' if node.flap_gate else 'NO'
                    f.write(f'{node.name:8}  {node.elevation:8.3f}    NORMAL    {msg:8}  {node.route_to}\n')
                if isinstance(node, OutfallFixed):
                    msg = 'YES' if node.flap_gate else 'NO'
                    f.write(
                        f'{node.name:8}  {node.elevation:8.3f}    FIXED    {node.stage:8}  {msg}  {node.route_to}\n')
                if isinstance(node, OutfallTidal):
                    msg = 'YES' if node.flap_gate else 'NO'
                    f.write(
                        f'{node.name:8}  {node.elevation:8.3f}    TIDAL    {node.tidal:8}  {msg}  {node.route_to}\n')
                if isinstance(node, OutfallTimeseries):
                    msg = 'YES' if node.flap_gate else 'NO'
                    f.write(
                        f'{node.name:8}  {node.elevation:8.3f}    TIMESERIES    {node.time_series:8}  {msg}  {node.route_to}\n')
            #
            f.write('\n\n[COORDINATES]\n')
            f.write(';;Name  X-Coord  Y-Coord\n')
            for node in self.node_list:
                f.write(f'{node.name:8}  {node.coordinate[0]:8.2f}  {node.coordinate[1]:8.2f}\n')
            #
            f.write('\n\n[DWF]\n')
            f.write(';;Node           Constituent      Baseline   Patterns  \n')
            for node in self.node_list:
                if isinstance(node, Junction):
                    if node.dwf_base_value != 0:
                        string = ' '.join(node.dwf_patterns)
                        f.write(f'{node.name}  FLOW  {node.dwf_base_value}  {string}\n')
        return 0

    def read_from_swmm_rpt(self, filename):
        for node in self.node_list:
            node.read_from_swmm_rpt(filename)


class Vertices:
    def __init__(self):
        self.link_name = None
        self.x = []
        self.y = []


class LinkResult:
    def __init__(self):
        self.date = []
        self.time = []  # in minutes
        self.flow = []
        self.velocity = []
        self.depth = []
        self.capacity = []


class Link:
    def __init__(self):
        self.name = ''
        self.vertices = Vertices()
        self.result = LinkResult()

    def read_from_swmm_rpt(self, filename):
        def time_text2minute(text):
            hours, minutes, seconds = text.split(':')
            result = int(minutes) + 60 * int(hours)
            return result

        # clear previous result
        self.result = LinkResult()
        #
        content = get_swmm_rpt_content(filename, f'Link {self.name}')
        for line in content:
            pair = line.split()
            self.result.date.append(pair[0])
            self.result.time.append(time_text2minute(pair[1]))
            self.result.flow.append(float(pair[2]))
            self.result.velocity.append(float(pair[3]))
            self.result.depth.append(float(pair[4]))
            self.result.capacity.append(float(pair[5]))


class Conduit(Link):
    def __init__(self):
        Link.__init__(self)
        self.upstream_node = ''
        self.downstream_node = ''
        self.length = 0.0
        self.roughness = 0.0
        self.upstream_offset = 0.0
        self.downstream_offset = 0.0
        # optional variable
        self.initial_flow = 0
        self.maximum_flow = 0  # means no limit


class ConduitCircle(Conduit):
    def __init__(self):
        Conduit.__init__(self)
        self.barrels_number = 1
        self.height = 0.0


class ConduitRectangleOpen(Conduit):
    def __init__(self):
        Conduit.__init__(self)
        self.barrels_number = 1
        self.height = 0.0
        self.width = 0.0


class ConduitCustom(Conduit):
    def __init__(self):
        Conduit.__init__(self)
        self.barrels_number = 1
        self.height = 0.0
        self.curve = ''


class LinkList:
    def __init__(self):
        self.link_list = []

    def add_link(self, link_type, link_information):
        def execute(func1, func2):
            def inner():
                new_link = func1()
                # basic information of conduit
                new_link.name = link_information['name']
                new_link.upstream_node = link_information['upstream_node']
                new_link.downstream_node = link_information['downstream_node']
                new_link.length = link_information['length']
                new_link.roughness = link_information['roughness']
                new_link.upstream_offset = link_information['upstream_offset']
                new_link.downstream_offset = link_information['downstream_offset']
                if 'initial_flow' in link_information:
                    new_link.initial_flow = link_information['initial_flow']
                if 'maximum_flow' in link_information:
                    new_link.maximum_flow = link_information['maximum_flow']
                # specific information of different conduit type
                func2(new_link)
                # add new link to link list
                self.link_list.append(new_link)
                return 0

            return inner

        match link_type:
            case 'conduit_circle':
                def conduit_circle(new_link):
                    new_link.height = link_information['height']
                    if 'barrels_number' in link_information:
                        new_link.barrels_number = link_information['barrels_number']

                return execute(ConduitCircle, conduit_circle)()

            case 'conduit_rectangle_open':
                def conduit_rectangle_open(new_link):
                    new_link.height = link_information['height']
                    new_link.width = link_information['width']
                    if 'barrels_number' in link_information:
                        new_link.barrels_number = link_information['barrels_number']

                return execute(ConduitRectangleOpen, conduit_rectangle_open)()

            case 'conduit_custom':
                def conduit_custom(new_link):
                    new_link.height = link_information['height']
                    new_link.curve = link_information['curve']
                    if 'barrels_number' in link_information:
                        new_link.barrels_number = link_information['barrels_number']

                return execute(ConduitCustom, conduit_custom)()

            case _:
                return -2

    def read_from_swmm_inp(self, filename):
        conduit_contents = get_swmm_inp_content(filename, '[CONDUITS]')
        # fill in default values
        for index, line in enumerate(conduit_contents):
            if len(line.split()) == 7:
                conduit_contents[index] += '  0  0'
            elif len(line.split()) == 8:
                conduit_contents[index] += '  0'
        x_section = get_swmm_inp_content(filename, '[XSECTIONS]')
        content = combine_swmm_inp_contents(conduit_contents, x_section)
        for line in content:
            pair = line.split()
            dic = {'name': pair[0], 'upstream_node': pair[1], 'downstream_node': pair[2], 'length': float(pair[3]),
                   'roughness': float(pair[4]), 'upstream_offset': float(pair[5]), 'downstream_offset': float(pair[6]),
                   'initial_flow': float(pair[7]), 'maximum_flow': float(pair[8])}

            match pair[9]:
                case 'CIRCULAR':
                    dic['height'] = float(pair[10])
                    # optional variable: Barrels
                    if len(pair) >= 15:
                        dic['barrels_number'] = int(pair[14])
                    self.add_link('conduit_circle', dic)

                case 'RECT_OPEN':
                    dic['height'] = float(pair[10])
                    dic['width'] = float(pair[11])
                    # optional variable: Barrels
                    if len(pair) >= 15:
                        dic['barrels_number'] = int(pair[14])
                    self.add_link('conduit_rectangle_open', dic)

                case 'CUSTOM':
                    dic['height'] = float(pair[10])
                    dic['curve'] = pair[11]
                    # optional variable: Barrels
                    if len(pair) >= 13:
                        dic['barrels_number'] = int(pair[-1])
                    self.add_link('conduit_custom', dic)
        #
        vertices_contents = get_swmm_inp_content(filename, '[VERTICES]')
        for line in vertices_contents:
            pair = line.split()
            for link in self.link_list:
                if link.name == pair[0]:
                    link.vertices.x.append(float(pair[1]))
                    link.vertices.y.append(float(pair[2]))
                    link.vertices.link_name = pair[0]
        return 0

    def write_to_swmm_inp(self, filename):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write('\n\n[CONDUITS]\n')
            f.write(
                ';;Name                          Upstream  Downstream  Length  Roughness  Up-offset Down-offset  Init_flow Max_flow\n')
            for link in self.link_list:
                f.write(
                    f'{link.name:30}  {link.upstream_node:8}  {link.downstream_node:8}  {link.length:8.2f}  {link.roughness:8.3f}  {link.upstream_offset:8.3f}  {link.downstream_offset:8.3f}  {link.initial_flow:8.2f}  {link.maximum_flow:8.2f}\n')
            #
            f.write('\n\n[XSECTIONS]\n')
            f.write(
                ';;Name                          Shape         Geom1      Geom2      Geom3      Geom4      Barrels      (Culvert)\n')
            for link in self.link_list:
                zero = 0
                if isinstance(link, ConduitCircle):
                    f.write(
                        f'{link.name:30}  CIRCULAR  {link.height:8.2f}  {zero:8}  {zero:8}  {zero:8}  {link.barrels_number:8}\n')
                if isinstance(link, ConduitRectangleOpen):
                    f.write(
                        f'{link.name:30}  RECT_OPEN {link.height:8.2f}  {link.width:8.2f}  {zero:8}  {zero:8}  {link.barrels_number:8}\n')
                if isinstance(link, ConduitCustom):
                    f.write(
                        f'{link.name:30}  CUSTOM    {link.height:8.2f}  {link.curve:8}  0  0  {link.barrels_number:8}\n')
            #
            f.write('\n\n[VERTICES]\n')
            f.write(';;Link           X-Coord            Y-Coord\n')
            for link in self.link_list:
                if link.vertices.link_name is not None:
                    for xi, yi in zip(link.vertices.x, link.vertices.y):
                        f.write(f'{link.vertices.link_name}  {xi}  {yi}\n')
        return 0

    def read_from_swmm_rpt(self, filename):
        for link in self.link_list:
            link.read_from_swmm_rpt(filename)


class InfiltrationHorton:
    def __init__(self):
        self.maximum_rate = 50  # mm/h
        self.minimum_rate = 5  # mm/h
        self.decay_rate = 5  # 1/h
        self.dry_time = 7  # day
        self.maximum_infiltration_volume = 0  # mm, 0 if not applicable


class InfiltrationGreenAmpt:
    def __init__(self):
        self.soil_capillary_suction = 0
        self.soil_saturated_hydraulic_conductivity = 0
        self.initial_soil_moisture_deficit = 0


class InfiltrationCurveNumber:
    def __init__(self):
        self.curve_number = 0
        self.dry_time = 0
        self.soil_saturated_hydraulic_conductivity = 0


class Infiltration:
    def __init__(self):
        self.horton = InfiltrationHorton()
        self.green_ampt = InfiltrationGreenAmpt()
        self.curve_number = InfiltrationCurveNumber()


class Polygon:
    def __init__(self):
        self.area_name = None
        self.x = []
        self.y = []


class Area:
    def __init__(self):
        self.name = ''
        self.rain_gage = ''
        self.outlet = ''
        #
        self.area = 0.0
        self.impervious_ratio = 0
        self.width = 0
        self.slope = 0
        #
        self.curb_length = 0
        self.snow_pack = ''
        #
        self.manning_impervious = 0
        self.manning_pervious = 0
        self.depression_impervious = 0
        self.depression_pervious = 0
        self.impervious_without_depression = 0
        #
        self.route_type = 'OUTLET'
        self.route_type_ratio = 100
        #
        self.infiltration = Infiltration()
        #
        self.polygon = Polygon()


class AreaList:
    def __init__(self):
        self.area_list = []

    def add_area(self, area_information):
        new_area = Area()
        if 'name' in area_information:
            new_area.name = area_information['name']
        if 'rain_gage' in area_information:
            new_area.rain_gage = area_information['rain_gage']
        if 'outlet' in area_information:
            new_area.outlet = area_information['outlet']
        #
        if 'area' in area_information:
            new_area.area = area_information['area']
        if 'impervious_ratio' in area_information:
            new_area.impervious_ratio = area_information['impervious_ratio']
        if 'width' in area_information:
            new_area.width = area_information['width']
        if 'slope' in area_information:
            new_area.slope = area_information['slope']
        #
        if 'curb_length' in area_information:
            new_area.curb_length = area_information['curb_length']
        if 'snow_pack' in area_information:
            new_area.snow_pack = area_information['snow_pack']
        #
        if 'manning_impervious' in area_information:
            new_area.manning_impervious = area_information['manning_impervious']
        if 'manning_pervious' in area_information:
            new_area.manning_pervious = area_information['manning_pervious']
        if 'depression_impervious' in area_information:
            new_area.depression_impervious = area_information['depression_impervious']
        if 'depression_pervious' in area_information:
            new_area.depression_pervious = area_information['depression_pervious']
        if 'impervious_without_depression' in area_information:
            new_area.impervious_without_depression = area_information['impervious_without_depression']
        #
        if 'route_type' in area_information:
            new_area.route_type = area_information['route_type']
        if 'route_type_ratio' in area_information:
            new_area.route_type_ratio = area_information['route_type_ratio']
        #
        if 'infiltration' in area_information:
            new_area.infiltration = area_information['infiltration']
        #
        #
        self.area_list.append(new_area)

    def read_from_swmm_inp(self, filename, infiltration_type='Horton'):
        sub_contents = get_swmm_inp_content(filename, '[SUBCATCHMENTS]')
        # fill in default values
        for index, line in enumerate(sub_contents):
            if len(line.split()) == 8:
                sub_contents[index] += '  VOID'
        #
        subarea_contents = get_swmm_inp_content(filename, '[SUBAREAS]')
        # fill in default values
        for index, line in enumerate(subarea_contents):
            if len(line.split()) == 7:
                subarea_contents[index] += '  100'
        content = combine_swmm_inp_contents(sub_contents, subarea_contents)
        #
        infiltration_contents = get_swmm_inp_content(filename, '[INFILTRATION]')
        content = combine_swmm_inp_contents(content, infiltration_contents)

        for line in content:
            pair = line.split()
            dic = {'name': pair[0],
                   'rain_gage': pair[1],
                   'outlet': pair[2],
                   'area': float(pair[3]),
                   'impervious_ratio': float(pair[4]),
                   'width': float(pair[5]),
                   'slope': float(pair[6]),
                   'curb_length': float(pair[7]),
                   'manning_impervious': float(pair[9]),
                   'manning_pervious': float(pair[10]),
                   'depression_impervious': float(pair[11]),
                   'depression_pervious': float(pair[12]),
                   'impervious_without_depression': float(pair[13]),
                   'route_type': pair[14]
                   }
            if dic['curb_length'] < 10e-5:
                dic['curb_length'] = int(0)
            #
            if pair[8] != 'VOID':
                dic['snow_pack'] = pair[8]
            if pair[15] != '100':
                dic['route_type_ratio'] = float(pair[15])
            #
            new_infiltration = Infiltration()

            match infiltration_type:
                case 'Horton':
                    new_infiltration.horton.maximum_rate = float(pair[16])
                    new_infiltration.horton.minimum_rate = float(pair[17])
                    new_infiltration.horton.decay_rate = float(pair[18])
                    new_infiltration.horton.decay_rate = float(pair[19])
                    new_infiltration.horton.maximum_infiltration_volume = float(pair[20])
                case 'GreenAmpt':
                    new_infiltration.green_ampt.soil_capillary_suction = float(pair[16])
                    new_infiltration.green_ampt.soil_saturated_hydraulic_conductivity = float(pair[17])
                    new_infiltration.green_ampt.initial_soil_moisture_deficit = float(pair[18])
                case 'CurveNumber':
                    new_infiltration.curve_number.curve_number = float(pair[16])
                    new_infiltration.curve_number.soil_saturated_hydraulic_conductivity = float(pair[17])
                    new_infiltration.curve_number.dry_time = float(pair[18])

            dic['infiltration'] = new_infiltration
            #
            self.add_area(dic)

        #
        polygon_contents = get_swmm_inp_content(filename, '[Polygons]')
        for line in polygon_contents:
            pair = line.split()
            for area in self.area_list:
                if area.name == pair[0]:
                    area.polygon.x.append(float(pair[1]))
                    area.polygon.y.append(float(pair[2]))
                    area.polygon.area_name = pair[0]
        return 0

    def write_to_swmm_inp(self, filename, infiltration_type='Horton'):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write('\n\n[SUBCATCHMENTS]\n')
            f.write(
                ';;Name       RainGage  Outlet     Area    %Imperv    Width    %Slope    CurbLen  (SnowPack)\n')
            for area in self.area_list:
                f.write(
                    f'{area.name}  {area.rain_gage}  {area.outlet}  {area.area:8.3f}  {area.impervious_ratio:8.2f}  {area.width:8.3f}  {area.slope:8.2f}  {area.curb_length:8}  {area.snow_pack}\n')
            #
            f.write('\n\n[SUBAREAS]\n')
            f.write(';;Subcatchment   N-Imperv   N-Perv  S-Imperv  S-Perv  PctZero  RouteTo  (PctRouted)\n')
            for area in self.area_list:
                if area.route_type_ratio != 100:
                    f.write(
                        f'{area.name}  {area.manning_impervious:8.3f}  {area.manning_pervious:8.2f}  {area.depression_impervious:8.2f}  {area.depression_pervious:8.2f}  {area.impervious_without_depression:8.2f}  {area.route_type:8}  {area.route_type_ratio:8}\n')
                else:
                    f.write(
                        f'{area.name}  {area.manning_impervious:8.3f}  {area.manning_pervious:8.2f}  {area.depression_impervious:8.2f}  {area.depression_pervious:8.2f}  {area.impervious_without_depression:8.2f}  {area.route_type:8}\n')
            #
            f.write('\n\n[INFILTRATION]\n')
            match infiltration_type:
                case 'Horton':
                    f.write(';;;;Subcatchment   MaxRate    MinRate    Decay      DryTime    MaxInfil \n')
                    for area in self.area_list:
                        f.write(
                            f'{area.name}  {area.infiltration.horton.maximum_rate:8.1f}  {area.infiltration.horton.minimum_rate:8.1f}  {area.infiltration.horton.decay_rate:8.1f}  {area.infiltration.horton.dry_time:8.1f}  {area.infiltration.horton.maximum_infiltration_volume:8.1f}\n')
                case 'GreenAmpt':
                    f.write(';;;;Subcatchment   \n')
                    for area in self.area_list:
                        f.write(
                            f'{area.name}  {area.infiltration.green_ampt.soil_capillary_suction:8}  {area.infiltration.green_ampt.soil_saturated_hydraulic_conductivity:8}  {area.infiltration.green_ampt.initial_soil_moisture_deficit:8}\n')
                case 'CurveNumber':
                    f.write(';;;;Subcatchment   \n')
                    for area in self.area_list:
                        f.write(
                            f'{area.name}  {area.infiltration.curve_number.curve_number:8}  {area.infiltration.curve_number.soil_saturated_hydraulic_conductivity:8}  {area.infiltration.curve_number.dry_time:8}\n')
            #
            f.write('\n\n[Polygons]\n')
            f.write(';;Subcatchment   X-Coord            Y-Coord\n')
            for area in self.area_list:
                if area.polygon.area_name is not None:
                    for xi, yi in zip(area.polygon.x, area.polygon.y):
                        f.write(f'{area.polygon.area_name}  {xi}  {yi}\n')
            return 0


class TimeSeries:
    def __init__(self):
        self.name = ''
        self.time = []  # in minutes
        self.value = []  # in mm


class RainGage:
    def __init__(self):
        self.name = ''
        self.form = ''
        self.interval = ''
        self.SCF = 1  # snow catch deficiency correction factor (use 1.0 for no adjustment)
        self.source = ''  # timeseries name


class Rain:
    def __init__(self):
        self.ts_list = []
        self.gage_list = []

    def add_ts(self, new_ts):
        self.ts_list.append(new_ts)

    def add_gage(self, new_gage):
        self.gage_list.append(new_gage)

    def read_from_swmm_inp(self, filename):
        # timeseries section
        def time_text2minute(text):
            hours, minutes = text.split(':')
            result = int(minutes) + 60 * int(hours)
            return result

        content = get_swmm_inp_content(filename, '[TIMESERIES]')
        this_timeseries = TimeSeries()
        this_timeseries.name = 'initial'
        for line in content:
            name, time, value = line.split()
            time = time_text2minute(time)
            value = float(value)

            if this_timeseries.name == 'initial':
                this_timeseries.name = name

            if this_timeseries.name != name:
                self.add_ts(this_timeseries)
                this_timeseries = TimeSeries()
                this_timeseries.name = name
                this_timeseries.time.append(time)
                this_timeseries.value.append(value)
            else:
                this_timeseries.time.append(time)
                this_timeseries.value.append(value)
        if this_timeseries.name != 'initial':
            self.add_ts(this_timeseries)
        # rain gage section
        content = get_swmm_inp_content(filename, '[RAINGAGES]')
        for line in content:
            name, form, interval, SCF, _, tise = line.split()
            this_gage = RainGage()
            this_gage.name = name
            this_gage.form = form
            this_gage.interval = interval
            this_gage.SCF = SCF
            this_gage.source = tise
            self.add_gage(this_gage)
        return 0

    def write_to_swmm_inp(self, filename):
        def time_minute2text(minutes):
            minutes = int(minutes)
            hours, left = divmod(minutes, 60)
            text = f'{hours}:{left:02}'
            return text

        with open(filename, 'a', encoding='utf-8') as f:
            f.write('\n\n[TIMESERIES]\n')
            f.write(';;Name       Time       Value\n')
            for ts in self.ts_list:
                for time, value in zip(ts.time, ts.value):
                    f.write(f'{ts.name}  {time_minute2text(time)}  {value}\n')
                f.write(';;\n')
            #
            f.write('\n\n[RAINGAGES]\n')
            f.write(';;Name  Format   Interval  SCF  Source    \n')
            for gage in self.gage_list:
                f.write(f'{gage.name}  {gage.form}  {gage.interval}  {gage.SCF}  TIMESERIES  {gage.source}\n')
            return 0


class Curve:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.x = []
        self.y = []


class Pattern:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.value = []


class ValueList:
    def __init__(self):
        self.curve_list = []
        self.pattern_list = []

    def add_curve(self, new_curve):
        self.curve_list.append(new_curve)

    def add_pattern(self, new_pattern):
        self.pattern_list.append(new_pattern)

    def read_from_swmm_inp(self, filename):
        #
        content = get_swmm_inp_content(filename, '[CURVES]')
        this_curve = Curve()
        this_curve.name = 'initial'
        for line in content:
            pair = line.split()
            name = pair[0]
            if this_curve.name == 'initial':
                this_curve.name = name
            if this_curve.name != name:
                self.add_curve(this_curve)
                this_curve = Curve()
                this_curve.name = name
            if len(pair) % 2 == 0:
                this_curve.type = pair[1]
                x_list = [float(i) for index, i in enumerate(pair[2::]) if index % 2 == 0]
                y_list = [float(i) for index, i in enumerate(pair[2::]) if index % 2 == 1]
            else:
                x_list = [float(i) for index, i in enumerate(pair[1::]) if index % 2 == 0]
                y_list = [float(i) for index, i in enumerate(pair[1::]) if index % 2 == 1]
            for x, y in zip(x_list, y_list):
                this_curve.x.append(x)
                this_curve.y.append(y)
        if this_curve.name != 'initial':
            self.add_curve(this_curve)
        #
        content = get_swmm_inp_content(filename, '[PATTERNS]')
        this_pattern = Pattern()
        this_pattern.name = 'initial'
        for line in content:
            pair = line.split()
            name = pair[0]
            if this_pattern.name == 'initial':
                this_pattern.name = name
            if this_pattern.name != name:
                self.add_pattern(this_pattern)
                this_pattern = Pattern()
                this_pattern.name = name
            if pair[1].isalpha():
                this_pattern.type = pair[1]
                for factor in pair[2::]:
                    this_pattern.value.append(factor)
            else:
                for factor in pair[1::]:
                    this_pattern.value.append(factor)
        if this_pattern.name != 'initial':
            self.add_pattern(this_pattern)
        return 0

    def write_to_swmm_inp(self, filename):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write('\n\n[CURVES]\n')
            f.write(';;Name           Type       X-Value    Y-Value  \n')
            for curve in self.curve_list:
                flag = 0
                for x, y in zip(curve.x, curve.y):
                    if flag == 0:
                        f.write(f'{curve.name}  {curve.type:8}  {x}  {y}\n')
                        flag = 1
                    else:
                        f.write(f'{curve.name}            {x}  {y}\n')
                f.write(';\n')
            #
            f.write('\n\n[PATTERNS]\n')
            f.write(';;Name           Type       Multipliers\n')
            for pattern in self.pattern_list:
                string = ' '.join(pattern.value)
                f.write(f'{pattern.name}  {pattern.type} {string}\n')
                f.write(';\n')
        return 0


class Udm:
    def __init__(self):
        # basic drainage model information
        self.name = 'My Urban Drainage Model'

        # calculation related information
        self.calc = CalculationInformation()

        # display related information
        self.disp = ''

        # entity related information
        self.link = LinkList()
        self.node = NodeList()
        self.area = AreaList()

        # rain related information
        self.rain = Rain()
        self.value = ValueList()

    def generate_swmm_inp(self, filename):
        self.calc.write_to_swmm_inp(filename)
        self.node.write_to_swmm_inp(filename)
        self.link.write_to_swmm_inp(filename)
        self.area.write_to_swmm_inp(filename)
        self.rain.write_to_swmm_inp(filename)
        self.value.write_to_swmm_inp(filename)
        return 0

    def read_from_swmm_inp(self, filename):
        self.calc.read_from_swmm_inp(filename)
        self.node.read_from_swmm_inp(filename)
        self.link.read_from_swmm_inp(filename)
        self.area.read_from_swmm_inp(filename)
        self.rain.read_from_swmm_inp(filename)
        self.value.read_from_swmm_inp(filename)
        return 0

    def execute(self):
        # create a temporary dictionary
        calculate_dir = pathlib.Path(pathlib.Path.cwd(), 'calculate_temp')
        if not calculate_dir.exists():
            calculate_dir.mkdir()

        # check execute file
        exe_file = pathlib.Path(calculate_dir, 'runswmm.exe')
        dll_file = pathlib.Path(calculate_dir, 'swmm5.dll')
        if not (exe_file.exists() and dll_file.exists()):
            import requests
            import zipfile
            # download
            download_link = 'https://github.com/USEPA/Stormwater-Management-Model/releases/download/v5.2.3/swmm-solver-5.2.3-win64.zip'
            download_file = requests.get(download_link)
            download_name = pathlib.Path(calculate_dir, 'swmm.zip')
            with open(download_name, 'wb') as file:
                file.write(download_file.content)
            # unpack
            unpack = zipfile.ZipFile(download_name)
            for names in unpack.namelist():
                unpack.extract(names, calculate_dir)
            unpack.close()
            # move file to target
            bin_dir = pathlib.Path(calculate_dir, 'swmm-solver-5.2.3-win64', 'bin')
            for each_file in bin_dir.glob('*.*'):
                each_file.rename(calculate_dir.joinpath(each_file.name))

        # make random tag
        tag = str(uuid.uuid4())

        # specify swmm inp file and report file
        inp_temp = pathlib.Path(calculate_dir, tag)
        self.generate_swmm_inp(str(inp_temp))

        rpt_name = tag + '.rpt'
        rpt_temp = pathlib.Path(calculate_dir, rpt_name)

        # run swmm and generate report.rpt file
        cmd = str(exe_file) + ' ' + str(inp_temp) + ' ' + str(rpt_temp)
        os.system(cmd)

        # read information into current object
        self.node.read_from_swmm_rpt(str(rpt_temp))
        self.link.read_from_swmm_rpt(str(rpt_temp))

        # remove temporary inp and report file
        inp_temp.unlink()
        rpt_temp.unlink()
