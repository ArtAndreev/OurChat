const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const core_src = path.resolve(__dirname, 'core', 'static', 'core', 'js');
const auth_src = path.resolve(__dirname, 'authentication', 'static', 'authentication', 'js');
const build = path.resolve(__dirname, 'build');

const isProd = process.env.NODE_ENV === 'production';
const publicPath = isProd ? '/static/' : '/assets/';


module.exports = {
    entry: {
        // vendor: ['jquery'],
        chat: path.resolve(core_src, 'chat.js'),
    },
    output: {
        path: build,
        filename: 'js/[name]-[hash].js',
    },
    plugins: [
        new BundleTracker({
            filename: 'webpack-stats.json'
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        }),
        new MiniCssExtractPlugin({
            filename: "css/[name]-[hash].css",
            chunkFilename: "css/[id].css"
        })
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader'
                }
            },
            {
                test: /\.(png|jpg|svg|ico)$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: 'img/[name]-[hash].[ext]'
                    }
                }
            },
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    !isProd ? MiniCssExtractPlugin.loader : 'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: !isProd,
                            importLoaders: 1,
                        }
                    },
                    {
                        loader: 'resolve-url-loader',
                        options: {
                            sourceMap: !isProd,
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: !isProd,
                        }
                    }
                ]
            }
        ]
    },
    devServer: {
        contentBase: build,
        compress: true,
        port: 8080
    }
};