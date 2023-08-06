import os
import datetime


class AutoLog:
    def __init__(self, name='', path='./'):
        if not os.path.exists(path+'logs'):
            os.mkdir(path+'logs')
        if name == '':
            self.__dir_name = path + 'logs' + '/log' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            self.__dir_name = path + 'logs' + '/' + name
        os.mkdir(self.__dir_name)
        os.mkdir(self.__dir_name + '/constant')
        os.mkdir(self.__dir_name + '/variable')
        self.__constant = ['hyper']
        self.__variable = ['metric']
        self.__variables = {}
        self.__need_best = {}
        self.__best = {}
        self.__start_time = 0

    def set_constant(self, *args):
        self.__constant = []
        for item in args:
            self.__constant.append(item)

    def set_variable(self, *args):
        self.__variable = []
        for item in args:
            self.__variable.append(item)

    def add_constant(self, *args):
        self.__constant = []
        for item in args:
            self.__constant.append(item)

    def add_variable(self, *args):
        self.__variable = []
        for item in args:
            self.__variable.append(item)

    def log_hyper(self, **kwargs):
        for k, v in kwargs.items():
            with open(self.__dir_name+'/constant/hyper.log', 'a') as f:
                f.write('{"hyper": {"'+k+'": '+str(v)+'}}\n')

    def log_constant(self, constant, **kwargs):
        if constant not in self.__constant:
            raise ValueError(constant+'不在constant列表内，请先使用add__constant(self, *args)进行添加')
        with open(self.__dir_name + '/constant/' + constant + '.log', 'a') as f:
            for k, v in kwargs.items():
                f.write('{"'+constant+'": {"'+k+'": '+str(v)+'}}\n')

    def log_metric(self, step, **kwargs):
        if 'metric' not in self.__variables:
            self.__variables['metric'] = []
        with open(self.__dir_name + '/variable/metric.log', 'a') as f:
            f.write('step: ' + str(step) + '    {"metric": ')
            comma = ''
            for k, v in kwargs.items():
                if k in self.__variables['metric']:
                    pass
                else:
                    self.__variables['metric'].append(k)
                f.write(comma+'{"'+k+'": '+str(v)+'}')
                comma = ', '
                if k in self.__need_best:
                    if k not in self.__best:
                        self.__best[k] = (0, v)
                    else:
                        if self.__need_best[k] == 'max':
                            if v > self.__best[k][1]:
                                self.__best[k] = (step, v)
                        else:
                            if v < self.__best[k][1]:
                                self.__best[k] = (step, v)
            f.write('}\n')

    def log_variable(self, variable, step, **kwargs):
        if variable not in self.__variables:
            self.__variables[variable] = []
        if variable not in self.__variable:
            raise ValueError(variable+'不在variable列表内，请先使用add__variable(self, *args)进行添加')
        with open(self.__dir_name + '/variable/'+variable+'.log', 'a') as f:
            f.write('step: ' + str(step) + '    {"'+variable+'": ')
            comma = ''
            for k, v in kwargs.items():
                if k in self.__variables[variable]:
                    pass
                else:
                    self.__variables[variable].append(k)
                f.write(comma+'{"'+k+'": '+str(v)+'}')
                comma = ', '
                if k in self.__need_best:
                    if k not in self.__best:
                        self.__best[k] = (0, v)
                    else:
                        if self.__need_best[k] == 'max':
                            if v > self.__best[k][1]:
                                self.__best[k] = (step, v)
                        else:
                            if v < self.__best[k][1]:
                                self.__best[k] = (step, v)
            f.write('}\n')

    def constant(self):
        return self.__constant

    def variable(self):
        return self.__variable

    def need_best(self, **kwargs):
        for k, v in kwargs.items():
            if v != 'max' and v != 'min':
                raise ValueError(v + '不是"max"或"min"的一种')
            self.__need_best[k] = v

    def log_best(self, *args):
        for variable in args:
            with open(self.__dir_name + '/variable/best__'+variable+'.log', 'a') as f:
                for item in self.__variables[variable]:
                    if item in self.__need_best:
                        f.write('step: ' + str(self.__best[item][0]) + '    {"' + variable + '": ' + ' {"' + item + '": ' + str(self.__best[item][1]) + '}}\n')

    def start(self):
        self.__start_time = datetime.datetime.now()

    def end(self):
        if self.__start_time == 0:
            raise AttributeError('请先用start函数开始计时')
        time = datetime.datetime.now() - self.__start_time
        time = time.total_seconds()
        with open(self.__dir_name + '/time.log', 'a') as f:
            f.write('{"time": '+str(time)+'}\n')

    def note(self, str):
        with open(self.__dir_name + '/note.txt', 'a') as f:
            f.write(str)
