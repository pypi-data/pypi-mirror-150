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
import { readFileSync } from 'fs';
import {
    isDemo,
    normalizeBookmark,
    normalizeDate,
    bookmarkToBase64,
    base64ToBookmark,
    bookmarkDiff,
    url2filename,
    PM_INCONSISTENT_KEYS
} from '../pagemarks/js/globals.js';


describe('The normalizeBookmark() function', () => {

    it('handles a simple small bookmark object', () => {
        let result = normalizeBookmark({
            name: "some name",
            url: "https://example.com"
        });
        expect(result).to.deep.equal({
            name: "some name",
            url: "https://example.com"
        });
    });


    it('trims whitespace from values', () => {
        const testDate = new Date();
        let result = normalizeBookmark({
            name: "some name  ",
            url: "\thttps://example.com",
            date_added: testDate,
            tags: [" tag1", "tag2 ", " tag3 ", "tag4"]
        });
        expect(result).to.deep.equal({
            name: "some name",
            url: "https://example.com",
            date_added: testDate,
            tags: ["tag1", "tag2", "tag3", "tag4"]
        });
    });


    it('removes empty values from the object completely', () => {
        const testDate = new Date();
        let result = normalizeBookmark({
            name: "  ",
            url: "https://example.com",
            date_added: testDate,
            tags: [],
            notes: ""
        });
        expect(result).to.deep.equal({
            url: "https://example.com",
            date_added: testDate
        });
    });
});


describe('The normalizeDate() function', () => {

    it('converts Date instances to strings', () => {
        let result = normalizeDate(new Date(1651408250 * 1000));
        expect(result).to.equal('2022-05-01 12:30:50');
    });

    it('omits the time component when it is zero', () => {
        let result = normalizeDate(new Date(1651363200 * 1000));
        expect(result).to.equal('2022-05-01');
    });

    it('raises an error when the date cannot be parsed', () => {
        const dummyDate = {
            toISOString: function() {
                return 'invalid';
            }
        };
        expect(() => normalizeDate(dummyDate)).to.throw('invalid date: invalid');
    });
});


describe('The bookmarkToBase64() function', () => {

    it('converts a bookmark object to base64 encoding with defined formatting', () => {
        let result = bookmarkToBase64({
            name: "some name",
            url: "https://example.com",
            date_added: new Date(1651408250 * 1000) // 2022-05-01 12:30:50 UTC
        });
        expect(result).to.equal(
            'ewogICAgIm5hbWUiOiAic29tZSBuYW1lIiwKICAgICJ1cmwiOiAiaHR0cHM6Ly9leGFtcGxlLmNv'
            + 'bSIsCiAgICAiZGF0ZV9hZGRlZCI6ICIyMDIyLTA1LTAxIDEyOjMwOjUwIgp9Cg==');
    });

    it('removes "id" fields if present', () => {
        let result = bookmarkToBase64({
            id: 'some-id',
            name: "some name",
            url: "https://example.com",
            date_added: new Date(1651408250 * 1000) // 2022-05-01 12:30:50 UTC
        });
        expect(result).to.equal(
            'ewogICAgIm5hbWUiOiAic29tZSBuYW1lIiwKICAgICJ1cmwiOiAiaHR0cHM6Ly9leGFtcGxlLmNv'
            + 'bSIsCiAgICAiZGF0ZV9hZGRlZCI6ICIyMDIyLTA1LTAxIDEyOjMwOjUwIgp9Cg==');
    });

    it('properly formats the tag list', () => {
        let result = bookmarkToBase64({
            name: "some name",
            url: "https://example.com",
            tags: ["tag1", "tag2", "tag3"]
        });
        expect(result).to.equal(
            'ewogICAgIm5hbWUiOiAic29tZSBuYW1lIiwKICAgICJ1cmwiOiAiaHR0cHM6Ly9leGFtcGxlLmNv'
            + 'bSIsCiAgICAidGFncyI6IFsidGFnMSIsICJ0YWcyIiwgInRhZzMiXQp9Cg==');
    });

    it('handles a very short tag list', () => {
        let result = bookmarkToBase64({
            url: "https://example.com",
            tags: ["x"]
        });
        expect(result).to.equal(
            'ewogICAgInVybCI6ICJodHRwczovL2V4YW1wbGUuY29tIiwKICAgICJ0YWdzIjogWyJ4Il0KfQo=');
    });

    it('produces UTF-8-encoded output', () => {
        let result = bookmarkToBase64({
            name: "Olé, Olé, Olé",
            url: "https://en.wikipedia.org/wiki/Ol%C3%A9,_Ol%C3%A9,_Ol%C3%A9"
        });
        expect(result).to.equal(
            'ewogICAgIm5hbWUiOiAiT2zDqSwgT2zDqSwgT2zDqSIsCiAgICAidXJsIjogImh0dHBzOi8vZW4u'
            + 'd2lraXBlZGlhLm9yZy93aWtpL09sJUMzJUE5LF9PbCVDMyVBOSxfT2wlQzMlQTkiCn0K');
    });
});


describe('The base64ToBookmark() function', () => {

    it('preserves the date values', () => {
        const inputJson = JSON.stringify({
            name: "some name",
            url: "https://example.com",
            date_added: "2021-08-15 12:30:02"
        });
        const input64 = Buffer.from(inputJson, 'binary').toString('base64');
        const result = base64ToBookmark(input64);
        expect(result).to.deep.equal({
            name: "some name",
            url: "https://example.com",
            date_added: new Date("2021-08-15 12:30:02")
        });
    });

    it('decodes UTF-8-encoded input', () => {
        const result = base64ToBookmark('ewogICAgIm5hbWUiOiAiT2zDqSwgT2zDqSwgT2zDqSIsCiAgICAidXJsIjogImh0dHBzOi8vZW4u'
            + 'd2lraXBlZGlhLm9yZy93aWtpL09sJUMzJUE5LF9PbCVDMyVBOSxfT2wlQzMlQTkiCn0K');
        expect(result).to.deep.equal({
            name: "Olé, Olé, Olé",
            url: "https://en.wikipedia.org/wiki/Ol%C3%A9,_Ol%C3%A9,_Ol%C3%A9"
        });
    });
});


describe('The bookmarkDiff() function', () => {

    it('finds added notes', () => {
        const bookmark1 = {
            name: "some name",
            url: "https://example.com",
            date_added: new Date("2021-08-15 12:30:02")
        };
        const bookmark2 = {
            name: "some name",
            url: "https://example.com",
            notes: "added notes",
            date_added: new Date("2021-08-15 12:30:02")
        };
        const result = bookmarkDiff(bookmark1, bookmark2);
        expect(result).to.deep.equal(['notes']);
    });

    it('finds added tags', () => {
        const bookmark1 = {
            name: "some name",
            url: "https://example.com",
            tags: ['tag1']
        };
        const bookmark2 = {
            name: "some name",
            url: "https://example.com",
            tags: ['tag1', 'tag2']
        };
        const result = bookmarkDiff(bookmark1, bookmark2);
        expect(result).to.deep.equal(['tags']);
    });

    it('finds that the "name" field was removed', () => {
        const bookmark1 = {
            name: "some name",
            url: "https://example.com",
            tags: ['tag1']
        };
        const bookmark2 = {
            url: "https://example.com",
            tags: ['tag1']
        };
        const result = bookmarkDiff(bookmark1, bookmark2);
        expect(result).to.deep.equal(['name']);
    });

    it('finds that the "tags" field was removed', () => {
        const bookmark1 = {
            url: "https://example.com",
            tags: ["tag1", "tag2"]
        };
        const bookmark2 = {
            url: "https://example.com"
        };
        const result = bookmarkDiff(bookmark1, bookmark2);
        expect(result).to.deep.equal(['tags']);
    });

    it('finds that a Date as Date and as string are inconsistent', () => {
        const bookmark1 = {
            name: "some name",
            url: "https://example.com",
            date_added: new Date("2021-08-15 12:30:02")
        };
        const bookmark2 = {
            name: "some name",
            url: "https://example.com",
            date_added: "2021-08-15 12:30:02"
        };
        const result = bookmarkDiff(bookmark1, bookmark2);
        expect(result).to.deep.equal([PM_INCONSISTENT_KEYS]);
    });

    it('finds that a Date as object and as Date are inconsistent', () => {
        const bookmark1 = {
            name: "some name",
            url: "https://example.com",
            date_added: new Date("2021-08-15 12:30:02")
        };
        const bookmark2 = {
            name: "some name",
            url: "https://example.com",
            date_added: { key: "some object" }
        };
        const result = bookmarkDiff(bookmark1, bookmark2);
        expect(result).to.deep.equal([PM_INCONSISTENT_KEYS]);
    });

    it('considers inconsistent keys as more important than other differences', () => {
        const bookmark1 = {
            name: "name1",
            url: "https://example.com",
            wrong: [2, 3, 4]
        };
        const bookmark2 = {
            name: "name2_CHANGED",   // not reported
            url: "https://example.com",
            wrong: "also wrong",     // reported as "inconsistent key"
            date_added: new Date("2021-08-15 12:30:02")     // not reported
        };
        const result = bookmarkDiff(bookmark1, bookmark2);
        expect(result).to.deep.equal([PM_INCONSISTENT_KEYS]);
    });

    it('reports multiple changed fields at once', () => {
        const bookmark1 = {
            name: "name1",
            url: "https://example.com",
            extra: [2, 3, 4]
        };
        const bookmark2 = {
            name: "name2_CHANGED",
            url: "https://example.com/also-changed",
            date_added: new Date("2021-08-15 12:30:02"),
            notes: "some new notes"
        };
        const result = bookmarkDiff(bookmark1, bookmark2).sort();
        expect(result).to.deep.equal(['date_added', 'extra', 'name', 'notes', 'url']);
    });

    it('recognizes inconsistency when one field is an object and the other object is really an array', () => {
        const bookmark1 = {
            name: "some name",
            url: "https://example.com",
            wrong: [2, 3, 4]
        };
        const bookmark2 = {
            name: "some name",
            url: "https://example.com",
            wrong: { field: "value" }
        };
        const result = bookmarkDiff(bookmark1, bookmark2);
        expect(result).to.deep.equal([PM_INCONSISTENT_KEYS]);
    });

    it('ignores properties inherited through the prototype chain', () => {
        function Bookmark1() {
            this.name = "some name";
            this.url = "https://example.com";
        }
        Bookmark1.prototype = { fromPrototype: "foo" };
        const bookmark1 = new Bookmark1();
        const bookmark2 = {
            name: "some name",
            url: "https://example.com"
        };
        const result = bookmarkDiff(bookmark1, bookmark2);
        expect(result).to.deep.equal([]);
    });

    it('handles undefined input parameters', () => {
        expect(bookmarkDiff(undefined, undefined)).to.deep.equal([]);
        expect(bookmarkDiff(undefined, {})).to.deep.equal([PM_INCONSISTENT_KEYS]);
        expect(bookmarkDiff({}, undefined)).to.deep.equal([PM_INCONSISTENT_KEYS]);
        expect(bookmarkDiff('foo', {})).to.deep.equal([PM_INCONSISTENT_KEYS]);
        expect(bookmarkDiff('foo', 'bar')).to.deep.equal([PM_INCONSISTENT_KEYS]);
    });

    it('reports same-type value differences only on known fields', () => {
        const bookmark1 = {
            name: "some name",  // known field
            url: "https://example.com",
            extra: "value"    // unknown field
        };
        const bookmark2 = {
            name: "name2_CHANGED",
            url: "https://example.com",
            extra: "CHANGED value"
        };
        const result = bookmarkDiff(bookmark1, bookmark2).sort();
        expect(result).to.deep.equal(['name']);
    });
});


describe('The isDemo() function', () => {

    it('defaults to false', () => {
        expect(isDemo()).to.be.false;
    });
});


describe('The url2filename() function', () => {

    const jsonData = readFileSync('./test/url_to_filename.json', 'utf-8');
    let spec = JSON.parse(jsonData);
    for (const url in spec) {
        it('computes \'' + spec[url] + '\' from \'' + url + '\'', () => {
            expect(url2filename(url)).to.equal(spec[url]);
        });
    }

    it('computes a result for an input string that is not a valid URL', () => {
        expect(url2filename('just some random data')).to.equal('03/t2j4muo2h3xsuabiyz5ito.json');
    });

    it('treats undefined input as invalid', () => {
        expect(url2filename(undefined)).to.equal('00/_______invalid________.json');
    });

    it('treats null input as invalid', () => {
        expect(url2filename(null)).to.equal('00/_______invalid________.json');
    });

    it('treats non-string input as invalid', () => {
        expect(url2filename([])).to.equal('00/_______invalid________.json');
    });

    it('works with the empty string', () => {
        expect(url2filename('')).to.equal('09/3i42h3s6nnfq2msvx7xzky.json');
    });
});
