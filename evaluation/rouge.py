# -*- coding: utf-8 -*-
__author__ = "Yuchen"
__aim__ = " "
__testCase__ = " "
from pyrouge import Rouge155
class Rouge(object):
    pass

def main():
    pass


if __name__ == '__main__':
    main()


    r = Rouge155()
    r.system_dir = 'test/system_summaries'
    r.model_dir = 'test/model_summaries'
    r.system_filename_pattern = 'some_name.(\d+).txt'
    r.model_filename_pattern = 'some_name.[A-Z].#ID#.txt'

    output = r.convert_and_evaluate()
    print(output)
    output_dict = r.output_to_dict(output)