'''
The Mixins used for unit tests for learner dashboard
'''
import httpretty
import json

from openedx.core.djangoapps.programs.models import ProgramsApiConfig


class ProgramsDataMixin(object):
    """Mixin mocking Programs API URLs and providing fake data for testing."""
    PROGRAM_NAMES = [
        'Test Program A',
        'Test Program B',
    ]

    COURSE_KEYS = [
        ['Org0', 'Course0', 'Run0'],
        ['Org0', 'Course0', 'Run1'],
        ['Org0', 'Course1', 'Run0'],
        ['Org0', 'Course1', 'Run1'],
        ['Org1', 'Course2', 'Run0'],
        ['Org1', 'Course2', 'Run1'],
        ['Org1', 'Course3', 'Run0'],
        ['Org1', 'Course3', 'Run1'],
    ]

    PROGRAMS_API_RESPONSE = {
        'results': [
            {
                'id': 1,
                'name': PROGRAM_NAMES[0],
                'subtitle': 'A program used for testing purposes',
                'category': 'xseries',
                'status': 'unpublished',
                'marketing_slug': '{}_test_url'.format(PROGRAM_NAMES[0].replace(' ', '_')),
                'organizations': [
                    {
                        'display_name': 'Test Organization 0',
                        'key': 'organization-0'
                    }
                ],
                'course_codes': [
                    {
                        'display_name': 'Test Course 0',
                        'key': 'course-0',
                        'organization': {
                            'display_name': 'Test Organization 0',
                            'key': 'organization-0'
                        },
                        'run_modes': [
                            {
                                'course_key': '/'.join(COURSE_KEYS[0]),
                                'mode_slug': 'verified',
                                'sku': '',
                                'start_date': '2015-11-05T07:39:02.791741Z',
                                'run_key': '0'
                            },
                            {
                                'course_key': '/'.join(COURSE_KEYS[1]),
                                'mode_slug': 'verified',
                                'sku': '',
                                'start_date': '2015-11-05T07:39:02.791741Z',
                                'run_key': '1'
                            }
                        ]
                    },
                    {
                        'display_name': 'Test Course 1',
                        'key': 'course-1',
                        'organization': {
                            'display_name': 'Test Organization 0',
                            'key': 'organization-0'
                        },
                        'run_modes': [
                            {
                                'course_key': '/'.join(COURSE_KEYS[2]),
                                'mode_slug': 'verified',
                                'sku': '',
                                'start_date': '2015-11-05T07:39:02.791741Z',
                                'run_key': '0'
                            },
                            {
                                'course_key': '/'.join(COURSE_KEYS[3]),
                                'mode_slug': 'verified',
                                'sku': '',
                                'start_date': '2015-11-05T07:39:02.791741Z',
                                'run_key': '1'
                            }
                        ]
                    }
                ],
                'created': '2015-10-26T17:52:32.861000Z',
                'modified': '2015-11-18T22:21:30.826365Z'
            },
            {
                'id': 2,
                'name': PROGRAM_NAMES[1],
                'subtitle': 'Another program used for testing purposes',
                'category': 'xseries',
                'status': 'unpublished',
                'marketing_slug': '{}_test_url'.format(PROGRAM_NAMES[1].replace(' ', '_')),
                'organizations': [
                    {
                        'display_name': 'Test Organization 1',
                        'key': 'organization-1'
                    }
                ],
                'course_codes': [
                    {
                        'display_name': 'Test Course 2',
                        'key': 'course-2',
                        'organization': {
                            'display_name': 'Test Organization 1',
                            'key': 'organization-1'
                        },
                        'run_modes': [
                            {
                                'course_key': '/'.join(COURSE_KEYS[4]),
                                'mode_slug': 'verified',
                                'sku': '',
                                'start_date': '2015-11-05T07:39:02.791741Z',
                                'run_key': '0'
                            },
                            {
                                'course_key': '/'.join(COURSE_KEYS[5]),
                                'mode_slug': 'verified',
                                'sku': '',
                                'start_date': '2015-11-05T07:39:02.791741Z',
                                'run_key': '1'
                            }
                        ]
                    },
                    {
                        'display_name': 'Test Course 3',
                        'key': 'course-3',
                        'organization': {
                            'display_name': 'Test Organization 1',
                            'key': 'organization-1'
                        },
                        'run_modes': [
                            {
                                'course_key': '/'.join(COURSE_KEYS[6]),
                                'mode_slug': 'verified',
                                'sku': '',
                                'start_date': '2015-11-05T07:39:02.791741Z',
                                'run_key': '0'
                            },
                            {
                                'course_key': '/'.join(COURSE_KEYS[7]),
                                'mode_slug': 'verified',
                                'sku': '',
                                'start_date': '2015-11-05T07:39:02.791741Z',
                                'run_key': '1'
                            }
                        ]
                    }
                ],
                'created': '2015-10-26T19:59:03.064000Z',
                'modified': '2015-10-26T19:59:18.536000Z'
            }
        ]
    }

    def mock_programs_api(self, data=None, status_code=200):
        """Utility for mocking out Programs API URLs."""
        self.assertTrue(httpretty.is_enabled(), msg='httpretty must be enabled to mock Programs API calls.')

        url = ProgramsApiConfig.current().internal_api_url.strip('/') + '/programs/'

        if data is None:
            data = self.PROGRAMS_API_RESPONSE

        body = json.dumps(data)

        httpretty.reset()
        httpretty.register_uri(httpretty.GET, url, body=body, content_type='application/json', status=status_code)
