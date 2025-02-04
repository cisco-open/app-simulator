import { describe, before, it, mock } from 'node:test';
import assert from 'node:assert';
import supertest from 'supertest';

import http from 'http';
import https from 'https';

import { createApp } from '../src/app.js';

describe('Test the app with example configurations', async () => {
    const logger = {
        debug: () => { },
        info: () => { },
        error: () => { },
        warn: () => { }
    }
    it('runs an app and returns a 404 for an empty config', (t, done) => {
        let app = createApp({
            'endpoints': {
                'http': {}
            },
        }, logger);
        supertest(app).get('/hello').expect(404).end(done)
    });
    it('runs an app and returns a valid response for a basic config', (t, done) => {
        let app = createApp({
            'endpoints': {
                'http': {
                    '/hello': [
                        "sleep,50",
                    ]
                }
            },
        }, logger);
        supertest(app).get('/hello').expect(200).then((response) => {
            assert.strictEqual(response.text, '["Slept for 50"]');
            done();
        });
    });
    it('runs an app and returns an error response for a basic config with error', (t, done) => {
        let app = createApp({
            'endpoints': {
                'http': {
                    '/hello': [
                        "error,500,This is an error"
                    ]
                }
            },
        }, logger);
        supertest(app).get('/hello').expect(500).then((response) => {
            assert.strictEqual(response.text, 'This is an error');
            done();
        });
    });
    it('writes a log for a basic config with a log message', (t, done) => {
        mock.method(logger, 'warn');
        let app = createApp({
            'endpoints': {
                'http': {
                    '/hello': [
                        "log,warn,This is a log message"
                    ]
                }
            },
        }, logger);
        supertest(app).get('/hello').expect(200).end(() => {
            assert.strictEqual(logger.warn.mock.callCount(), 1);
            done();
        })
    });
    it('returns some HTML based on the configuration', (t, done) => {
        mock.method(logger, 'warn');
        let app = createApp({
            'endpoints': {
                'http': {
                    '/hello': [
                        "image,/image.jpg",
                        "script,/script.js",
                        "ajax,/ajax.json"
                    ]
                }
            },
        }, logger);
        supertest(app).get('/hello').expect(200).then((response) => {
            assert.strictEqual(response.text, '["<img src=\'/image.jpg\' />","<script src=\'/script.js?output=javascript\'></script>","<script>var o = new XMLHttpRequest();o.open(\'GET\', \'/ajax.json\');o.send();</script>"]');
            done();
        })
    });
    it('connects with a remote service for HTTP calls', (t, done) => {
        // Mock http.request
        mock.method(http, 'get', (options, callback) => {
            const mockResponse = new http.IncomingMessage();
            mockResponse.statusCode = 200;
            mockResponse.headers = { 'content-type': 'application/json' };

            process.nextTick(() => {
                callback(mockResponse);
                mockResponse.emit('data', 'Hello from example');
                mockResponse.emit('end');
            });

            return new http.ClientRequest();
        });
        let app = createApp({
            'endpoints': {
                'http': {
                    '/hello': [
                        "http://example/hello",
                        "https://mockservice/echo"
                    ]
                }
            },
        }, logger);
        supertest(app).get('/hello').expect(200).then((response) => {
            assert.strictEqual(http.get.mock.callCount(), 2);
            assert.strictEqual(response.text, '["Hello from example","Hello from example"]');
            done();
        });
    });
}); 