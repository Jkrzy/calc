import re

from .util import CfTestCase


class CloudFrontTests(CfTestCase):
    def test_app_is_fronted_by_cloudfront(self):
        '''
        This just makes sure our app is actually being fronted by
        AWS CloudFront.
        '''

        res = self.client.get('/blarg')
        self.assertIn('X-Amz-Cf-Id', res.headers)

    def test_index_has_short_expiry(self):
        '''
        Mitigation against https://github.com/18F/calc/issues/1257.
        '''

        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Cache-Control'],
                         'max-age=0')

    def test_static_files_have_long_expiry(self):
        '''
        This ensures that our static files have a very long expiry,
        which should be the case since the hash of their contents is
        part of their URL.
        '''

        res = self.client.get(
            # This particular file will rarely, if ever, change, so
            # we'll just hardcode its hash here.
            '/static/frontend/images/flag-usa.9db9ec00aaa0.png'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Cache-Control'],
                         'public, max-age=315360000')

    def test_ajaxform_submission_works(self):
        '''
        This basically ensures that the 'X-Requested-With' header is
        being passed through, so that our progressively-enhanced Ajax forms
        can detect whether they're being accessed via Ajax or not.
        '''

        self.browser.open('/styleguide/ajaxform')
        self.browser.session.headers['Referer'] = self.ORIGIN
        self.browser.session.headers['X-Requested-With'] = 'XMLHttpRequest'
        form = self.browser.get_form()
        self.browser.submit_form(form)
        self.assertEqual(self.browser.response.status_code, 200)
        self.assertIn('form_html', self.browser.response.json())

    def test_form_submission_works(self):
        '''
        Mitigation against https://github.com/18F/calc/issues/1198.
        '''

        self.browser.open('/styleguide/radio-checkbox')
        self.browser.session.headers['Referer'] = self.ORIGIN
        form = self.browser.get_form()
        form['radios'].value = '2'
        form['checkboxes'].value = 'a'
        self.browser.submit_form(form)
        self.assertEqual(self.browser.response.status_code, 200)
        self.assertIn('You chose radio option #2!',
                      self.browser.response.content.decode('utf-8'))

    def test_api_supports_cors(self):
        '''
        Mitigation against https://github.com/18F/calc/issues/1307.
        '''

        res = self.client.get('/')
        m = re.search(r'var API_HOST = "([^"]+)"',
                      res.content.decode('utf-8'))
        api_url = m.group(1)

        res = self.client.get(
            api_url + 'search/?format=json&q=zzzzzzzz&query_type=match_all',
            headers={'Origin': self.ORIGIN}
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), [])
        self.assertEqual(res.headers['Access-Control-Allow-Origin'], '*')
