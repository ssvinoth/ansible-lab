#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: deep_diff
short_description: Does a deep diff of dictionaries
version_added: "1.0"
description:
    - "Calculate differences between dictionries. It uses deepdiff python module from zepworks"
options:
    first_object:
        description:
            - First Dictionary Object.
        required: true
        type: dict
    second_object:
        description:
            - Second Dictionary Object.
        required: true
        type: dict
      
author:
    - Vinoth Kumar (@ssvinoth)
'''

EXAMPLES = '''
# Compare two dict objects

- name: Calling hello_message module
  deep_diff:
    first_object: "{{ firstobj }}"
    second_object: "{{ secondobj }}"
  vars:
    firstobj:
      val1: 'jsdfsdf'
      val2:
        - vv1
        - vv2
      val3:
        val31: 'nansdsd'
        val32:
          - val321:
              val3211: 'firstval'
              val3212: 'secondval'
          - val322:
              val3221: 'thirdval'
              val3222: 'fourthval'
    secondobj:
      val1: 'jsdfsdf'
      val2:
        - vv2
        - vv1
      val3:
        val31: 'nansdsd'
        val32:
          - val321:
              val3212: 'secondval'
              val3211: 'firstval'
          - val322:
              val3222: 'fourthval'      
              val3221: 'thirdval'
'''

RETURN = '''
values_changed:
    description: Dictionary containing all the difference in values
    returned: success
    type: dict
    sample: |
        'values_changed': {
                            "root['val3']['val31']": {'new_value': 'nansdsd1', 'old_value': 'nansdsd'},
                            "root['val3']['val32'][0]['val321']['val3212']": {'new_value': 'secondval','old_value': 'secondval2'}
                          }
        
is_same:
    description: Boolean to state if the provided two objects are same
    returned: success
    type: bool
    sample: |
        is_same: true 
'''

from ansible.module_utils.basic import AnsibleModule
from deepdiff import DeepDiff
from pprint import pprint


def main():

    module_args = dict(
        first_object=dict(type='dict', required=True),
        second_object=dict(type='dict', required=True),
    )
    result = dict(
        changed=False,
        values_changed={},
        is_same=True
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    # if check mode
    if module.check_mode:
        module.exit_json(**result)
    try:
        # Do a Diff 
        ddiff=DeepDiff(module.params['first_object'],module.params['second_object'], ignore_order=True, cutoff_distance_for_pairs=1, cutoff_intersection_for_pairs=1)
        pprint(ddiff)
        
        if not ddiff:
            result['is_same'] = True          
        else:
            result['is_same'] = False
        
        result['values_changed'] = ddiff
        result['changed'] = True
        module.exit_json(**result)
    except:
       module.fail_json(msg='Failed while calculating diff', **result)     


if __name__ == "__main__":
    main()