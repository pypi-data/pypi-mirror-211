from markdown.test_tools import TestCase


class TestBadge(TestCase):

    maxDiff = None

    def test_with_lists(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                - List
                    List {{ note "Badge" }}
                - Paragraph
                    Paragraph
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>
                <p>List</p>
                <p>List <span class="badge note"><span class="badge-title">Badge</span></span></p>
                </li>
                <li>
                <p>Paragraph</p>
                <p>Paragraph</p>
                </li>
                </ul>
                '''
            ),
            extensions=['badge']
        )

    def test_definition_list(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                Term
                :   Definition {{ note "Badge" }}
                    More text
                :   Another
                    definition
                    Even more text
                '''
            ),
            self.dedent(
                '''
                <dl>
                <dt>Term</dt>
                <dd>
                <p>Definition <span class="badge note"><span class="badge-title">Badge</span></span></p>
                <p>More text</p>
                </dd>
                <dd>
                <p>Another
                definition</p>
                <p>Even more text</p>
                </dd>
                </dl>
                '''
            ),
            extensions=['badge', 'def_list']
        )

    def test_with_preceding_text(self):
        self.assertMarkdownRenders(
            'foo **foo** {{ note "Badge" }}',
            '<p>foo <strong>foo</strong> <span class="badge note"><span class="badge-title">Badge</span></span></p>',
            extensions=['badge']
        )