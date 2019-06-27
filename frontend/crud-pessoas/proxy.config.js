const proxy = [
    {
        context: '/',
        target: 'http://0.0.0.0:5000',
        pathRewrite: { '^/': '' }
    }
];
module.exports = proxy;