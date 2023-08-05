(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['exports', 'echarts'], factory);
    } else if (
        typeof exports === 'object' &&
        typeof exports.nodeName !== 'string'
    ) {
        // CommonJS
        factory(exports, require('echarts'));
    } else {
        // Browser globals
        factory({}, root.echarts);
    }
})(this, function(exports, echarts) {
    var log = function(msg) {
        if (typeof console !== 'undefined') {
            console && console.error && console.error(msg);
        }
    };
    if (!echarts) {
        log('ECharts is not Loaded');
        return;
    }

    var colorPalette = [
        '#f2385a',
        '#f5a503',
        '#4ad9d9',
        '#f7879c',
        '#c1d7a8',
        '#4dffd2',
        '#fccfd7',
        '#d5f6f6'
    ];

    var theme = {
        color: colorPalette,

        title: {
            textStyle: {
                fontWeight: 'normal',
                color: '#f2385a'
            }
        },

        visualMap: {
            color: ['#f2385a', '#f5a503']
        },

        toolbox: {
            color: ['#f2385a', '#f2385a', '#f2385a', '#f2385a']
        },

        tooltip: {
          //  backgroundColor: 'rgba(0,0,0,0.5)',
            axisPointer: {
                // Axis indicator, coordinate trigger effective
                type: 'line', // The default is a straight line： 'line' | 'shadow'
                lineStyle: {
                    // Straight line indicator style settings
                    color: '#f2385a',
                    type: 'dashed'
                },
                crossStyle: {
                    color: '#f2385a'
                },
                shadowStyle: {
                    // Shadow indicator style settings
                    color: 'rgba(200,200,200,0.3)'
                }
            }
        },

        // Area scaling controller
        dataZoom: {
            dataBackgroundColor: '#eee', // Data background color
            fillerColor: 'rgba(200,200,200,0.2)', // Fill the color
            handleColor: '#f2385a' // Handle color
        },

        timeline: {
            lineStyle: {
                color: '#f2385a'
            },
            controlStyle: {
                color: '#f2385a',
                borderColor: '#f2385a'
            }
        },

        candlestick: {
            itemStyle: {
                color: '#f2385a',
                color0: '#f5a503'
            },
            lineStyle: {
                width: 1,
                color: '#f2385a',
                color0: '#f5a503'
            },
            areaStyle: {
                color: '#c1d7a8',
                color0: '#4ad9d9'
            }
        },

        map: {
            itemStyle: {
                color: '#f2385a'
            },
            areaStyle: {
                color: '#ddd'
            },
            label: {
                color: '#c12e34'
            }
        },

        graph: {
            itemStyle: {
                color: '#f2385a'
            },
            linkStyle: {
                color: '#f2385a'
            }
        },

        gauge: {
            axisLine: {
                lineStyle: {
                    color: [
                        [0.2, '#f5a503'],
                        [0.8, '#f2385a'],
                        [1, '#c1d7a8']
                    ],
                    width: 8
                }
            }
        }
    };

    echarts.registerTheme('azul', theme);
});