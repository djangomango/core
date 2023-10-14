const path = require('path');
const baseConfig = require('./webpack.common.config.js');
const { merge } = require('webpack-merge');
const Dotenv = require('dotenv-webpack');
var BundleTracker = require('webpack-bundle-tracker');
var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = merge(baseConfig, {
    mode: 'development',
    output: {
        path: path.resolve('../staticfiles/build/'),
    },
    devServer: {
        devMiddleware: {
            writeToDisk: true,
        },
    },
    watchOptions: {
        aggregateTimeout: 300,
        poll: 1000,
    },
    plugins: [
        new Dotenv({
            path: './.env.dev',
        }),
        new BundleTracker({
            path: __dirname,
            filename: 'webpack-stats.dev.json',
        }),
        new BundleAnalyzerPlugin(),
    ],
});
