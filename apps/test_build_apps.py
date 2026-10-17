import os, sys, unittest
sys.path.insert(0, os.path.dirname(__file__))
import build_apps as b

class T(unittest.TestCase):
    def test_norm(self):
        self.assertEqual(b.norm_rule('DOMAIN-SUFFIX,Claude.AI'), ('DOMAIN-SUFFIX', 'claude.ai'))
        self.assertEqual(b.norm_rule('IP-CIDR,160.79.104.1/21,no-resolve'), ('IP-CIDR', '160.79.104.0/21'))
        self.assertEqual(b.norm_rule('PROCESS-NAME,x')[0], 'DROP')
        self.assertIsNone(b.norm_rule('# c'))
    def test_dedupe_suffix(self):
        r = b.dedupe([('DOMAIN-SUFFIX', 'a.com'), ('DOMAIN', 'x.a.com'), ('DOMAIN-SUFFIX', 'b.a.com'), ('DOMAIN', 'a.org')])
        self.assertEqual(r, [('DOMAIN-SUFFIX', 'a.com'), ('DOMAIN', 'a.org')])
    def test_cover(self):
        self.assertEqual(b.covered_by(('DOMAIN', 'api.x.com'), {'x.com'}), ('DOMAIN-SUFFIX', 'x.com'))
        self.assertIsNone(b.covered_by(('DOMAIN', 'xx.com'), {'x.com'}))
    def test_manifest_unique(self):
        ids = [a['id'] for a in b.MAN['apps']]
        self.assertEqual(len(ids), len(set(ids)))

if __name__ == '__main__':
    unittest.main()
