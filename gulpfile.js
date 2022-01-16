/**
 * Install with 
 * npm install
 * 
 * Run with
 * gulp
 * to watch changes reflected on http://localhost:3002/
 */

const gulp = require("gulp");
const browserSync = require('browser-sync').create();
var exec = require('child_process').exec;

function makeHtml() {
    const cmd = 'make html';
    return new Promise((resolve, reject) => {
        exec(cmd, (error, stdout, stderr) => {
            if (error) {
                console.error(error);
                reject(error);
            }
            resolve(stdout? stdout : stderr);
        });
    });
}

function buildAndBrowserSync(done) {
    makeHtml().then(function() {
        browserSync.reload();
    }, function(Error) {
        console.log(Error);
    });
    done();
}

function watch() {
    browserSync.init({
        server: {
            baseDir: '_build/html/'
        },
        port: 3002,
        ui: {
            port: 3003
        },
    });
    gulp.watch(['docs/**/*.rst', 'docs/**/*.md',], buildAndBrowserSync);
}

// presentation
function makePresentation() {
    const cmd = 'make presentation';
    return new Promise((resolve, reject) => {
        exec(cmd, (error, stdout, stderr) => {
            if (error) {
                console.error(error);
                reject(error);
            }
            resolve(stdout? stdout : stderr);
        });
    });
}

function buildAndBrowserSyncPresentation(done) {
    makePresentation().then(function() {
        browserSync.reload();
    }, function(Error) {
        console.log(Error);
    });
    done();
}

function watchPresentation() {
    browserSync.init({
        server: {
            baseDir: '_build/presentation/'
        },
        port: 3002,
        ui: {
            port: 3003
        },
    });
    gulp.watch(['docs/**/*.rst', 'docs/**/*.md',], buildAndBrowserSyncPresentation);
}

exports.presentation = watchPresentation;
exports.default = watch;
