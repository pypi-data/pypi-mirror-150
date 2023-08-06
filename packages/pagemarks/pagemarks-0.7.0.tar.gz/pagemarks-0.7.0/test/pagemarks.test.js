/*
 * pagemarks - Free, git-backed, self-hosted bookmarks
 * Copyright (c) 2019-2021 the pagemarks contributors
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
 * License, version 3, as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.
 * If not, see <https://www.gnu.org/licenses/gpl.html>.
 */

'use strict';

import { expect } from 'chai';
import { describe } from 'mocha';
import { parseQuery } from '../pagemarks/js/pagemarks.js';


describe('The parseQuery() function', () => {

    it('handles empty input', () => {
        let result = parseQuery('');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal([]);
        expect(result.tags).to.deep.equal([]);

        result = parseQuery(' ');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal([]);
        expect(result.tags).to.deep.equal([]);

        result = parseQuery(' \t ');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal([]);
        expect(result.tags).to.deep.equal([]);

        result = parseQuery('\t');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal([]);
        expect(result.tags).to.deep.equal([]);
    });


    it('handles null and undefined input', () => {
        let result = parseQuery(null);
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal([]);
        expect(result.tags).to.deep.equal([]);

        result = parseQuery(undefined);
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal([]);
        expect(result.tags).to.deep.equal([]);
    });


    it('treats a single character as one short word', () => {
        let result = parseQuery('x');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['x']);
        expect(result.tags).to.deep.equal([]);
    });


    it('recognizes a simple, single word', () => {
        let result = parseQuery('foo');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo']);
        expect(result.tags).to.deep.equal([]);
    });


    it('ignores leading and trailing whitespace', () => {
        let result = parseQuery('foo   ');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo']);
        expect(result.tags).to.deep.equal([]);

        result = parseQuery('    foo');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo']);
        expect(result.tags).to.deep.equal([]);
    });


    it('treats quoted words as one, even if it contains whitespace', () => {
        let result = parseQuery('"foo bar"');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo bar']);
        expect(result.tags).to.deep.equal([]);
    });


    it('handles a mixture of tags and words', () => {
        let result = parseQuery('"foo" "bar boo" [tag1]word [tag2] bar');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo', 'bar boo', 'word', 'bar']);
        expect(result.tags).to.deep.equal(['tag1', 'tag2']);
    });


    it('treats closing tag bracket as word boundary', () => {
        let result = parseQuery('foo [tag]bar');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo', 'bar']);
        expect(result.tags).to.deep.equal(['tag']);
    });


    it('recognizes words which were started quoted but not closed', () => {
        let result = parseQuery('"foobar');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foobar']);
        expect(result.tags).to.deep.equal([]);
    });


    it('removes quotes from a single quoted word', () => {
        let result = parseQuery('"foo"');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo']);
        expect(result.tags).to.deep.equal([]);
    });


    it('removes brackets from a single tag', () => {
        let result = parseQuery('[tag]');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal([]);
        expect(result.tags).to.deep.equal(['tag']);
    });


    it('treats unclosed tags as words (without its opening tag bracket)', () => {
        let result = parseQuery('[tag');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['tag']);
        expect(result.tags).to.deep.equal([]);
    });


    it('treats quotes and opening brackets enclosed in words as part of the word', () => {
        let result = parseQuery('foo"b[ar');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo"b[ar']);
        expect(result.tags).to.deep.equal([]);
    });


    it('assigns no special meaning to closing brackets when no opening bracket was present', () => {
        let result = parseQuery('foo tag]');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo', 'tag]']);
        expect(result.tags).to.deep.equal([]);
    });


    it('assigns no special meaning to closing quotes when no opening quote was present', () => {
        let result = parseQuery('foo bar"');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo', 'bar"']);
        expect(result.tags).to.deep.equal([]);
    });


    it('correctly handles escaped quotes', () => {
        let result = parseQuery('foo "bar\\\\\"boo far" "boo\\\""');
        expect(result).to.not.be.null;
        expect(result.words).to.deep.equal(['foo', 'bar\\\\\"boo far', 'boo\\\"']);
        expect(result.tags).to.deep.equal([]);
    });
});
