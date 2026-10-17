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
    def test_v4_every_cn_rule_assigned(self):
        v = b.v4_index()
        got = set(v['common']) | {r for r, _ in v['intl_only']}
        for d in (v['own'], v['dep']):
            for rules in d.values(): got |= set(rules)
        self.assertEqual(set(v['universe']) - got, set())
    def test_v4_family_shared(self):
        # 只被腾讯系多个 App 共同认领的条目应归 CN-Tencent，而不是某个单 App
        fam = {a['id']: a.get('family') for a in b.MAN['apps']}
        self.assertEqual(fam.get('CN-QQ'), 'CN-Tencent')
        self.assertEqual(fam.get('CN-AppleMusic'), 'CN-Apple')
        v = b.v4_index()
        self.assertGreater(len(v['own'].get('CN-Apple', [])), 0)
    def test_v4_ids_unique(self):
        ids = [i for a in b.MAN['apps'] for i in a.get('v4_app_ids', [])]
        self.assertEqual(len(ids), len(set(ids)))
    def test_ip_fragment_keyword(self):
        self.assertTrue(b.IP_FRAGMENT.match('101.226.129.'))
        self.assertFalse(b.IP_FRAGMENT.match('alipay'))

if __name__ == '__main__':
    unittest.main()
