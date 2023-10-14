const path = require('path');
const baseConfig = require('./webpack.common.config.js');
const { merge } = require('webpack-merge');
const Dotenv = require('dotenv-webpack');
var BundleTracker = require('webpack-bundle-tracker');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = merge(baseConfig, {
    mode: 'production',
    output: {
        path: path.resolve('../static/build/'),
    },
    devServer: {
        devMiddleware: {
            writeToDisk: true,
        },
    },
    plugins: [
        new Dotenv({
            path: './.env.prod',
        }),
        new BundleTracker({
            path: __dirname,
            filename: 'webpack-stats.prod.json',
        }),
    ],
    optimization: {
        minimizer: [`...`, new CssMinimizerPlugin()],
    },
});
