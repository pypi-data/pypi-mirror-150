/******/ (function() { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./nikas/js/app/api.js":
/*!*****************************!*\
  !*** ./nikas/js/app/api.js ***!
  \*****************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

var Q = __webpack_require__(/*! app/lib/promise */ "./nikas/js/app/lib/promise.js");
var globals = __webpack_require__(/*! app/globals */ "./nikas/js/app/globals.js");

("use strict");

var salt = "Eech7co8Ohloopo9Ol6baimi",
    location = function () {
        return window.location.pathname;
    };

var script,
    endpoint,
    js = document.getElementsByTagName("script");

// prefer `data-nikas="//host/api/endpoint"` if provided
for (var i = 0; i < js.length; i++) {
    if (js[i].hasAttribute("data-nikas")) {
        endpoint = js[i].getAttribute("data-nikas");
        break;
    }
}

// if no async-script is embedded, use the last script tag of `js`
if (!endpoint) {
    for (i = 0; i < js.length; i++) {
        if (js[i].getAttribute("async") || js[i].getAttribute("defer")) {
            throw (
                "Nikas's automatic configuration detection failed, please " +
                "refer to https://docs.nikasproject.ir/config/client.html " +
                "and add a custom `data-nikas` attribute."
            );
        }
    }

    script = js[js.length - 1];
    endpoint = script.src.substring(
        0,
        script.src.length - "/js/embed.min.js".length
    );
}

//  strip trailing slash
if (endpoint[endpoint.length - 1] === "/") {
    endpoint = endpoint.substring(0, endpoint.length - 1);
}

var curl = function (method, url, data, resolve, reject) {
    var xhr = new XMLHttpRequest();

    function onload() {
        var date = xhr.getResponseHeader("Date");
        if (date !== null) {
            globals.offset.update(new Date(date));
        }

        var cookie = xhr.getResponseHeader("X-Set-Cookie");
        if (cookie && cookie.match(/^nikas-/)) {
            document.cookie = cookie;
        }

        if (xhr.status >= 500) {
            if (reject) {
                reject(xhr.body);
            }
        } else {
            resolve({ status: xhr.status, body: xhr.responseText });
        }
    }

    try {
        xhr.open(method, url, true);
        xhr.withCredentials = true;
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                onload();
            }
        };
    } catch (exception) {
        (reject || console.log)(exception.message);
    }

    xhr.send(data);
};

var qs = function (params) {
    var rv = "";
    for (var key in params) {
        if (
            params.hasOwnProperty(key) &&
            params[key] !== null &&
            typeof params[key] !== "undefined"
        ) {
            rv += key + "=" + encodeURIComponent(params[key]) + "&";
        }
    }

    return rv.substring(0, rv.length - 1); // chop off trailing "&"
};

var create = function (tid, data) {
    var deferred = Q.defer();
    curl(
        "POST",
        endpoint + "/new?" + qs({ uri: tid || location() }),
        JSON.stringify(data),
        function (rv) {
            if (rv.status === 201 || rv.status === 202) {
                deferred.resolve(JSON.parse(rv.body));
            } else {
                deferred.reject(rv.body);
            }
        }
    );
    return deferred.promise;
};

var modify = function (id, data) {
    var deferred = Q.defer();
    curl("PUT", endpoint + "/id/" + id, JSON.stringify(data), function (rv) {
        if (rv.status === 403) {
            deferred.reject("Not authorized to modify this comment!");
        } else if (rv.status === 200) {
            deferred.resolve(JSON.parse(rv.body));
        } else {
            deferred.reject(rv.body);
        }
    });
    return deferred.promise;
};

var remove = function (id) {
    var deferred = Q.defer();
    curl("DELETE", endpoint + "/id/" + id, null, function (rv) {
        if (rv.status === 403) {
            deferred.reject("Not authorized to remove this comment!");
        } else if (rv.status === 200) {
            deferred.resolve(JSON.parse(rv.body) === null);
        } else {
            deferred.reject(rv.body);
        }
    });
    return deferred.promise;
};

var view = function (id, plain) {
    var deferred = Q.defer();
    curl(
        "GET",
        endpoint + "/id/" + id + "?" + qs({ plain: plain }),
        null,
        function (rv) {
            deferred.resolve(JSON.parse(rv.body));
        }
    );
    return deferred.promise;
};

var fetch = function (tid, limit, nested_limit, parent, lastcreated) {
    if (typeof limit === "undefined") {
        limit = "inf";
    }
    if (typeof nested_limit === "undefined") {
        nested_limit = "inf";
    }
    if (typeof parent === "undefined") {
        parent = null;
    }

    var query_dict = {
        uri: tid || location(),
        after: lastcreated,
        parent: parent,
    };

    if (limit !== "inf") {
        query_dict["limit"] = limit;
    }
    if (nested_limit !== "inf") {
        query_dict["nested_limit"] = nested_limit;
    }

    var deferred = Q.defer();
    curl("GET", endpoint + "/?" + qs(query_dict), null, function (rv) {
        if (rv.status === 200) {
            deferred.resolve(JSON.parse(rv.body));
        } else if (rv.status === 404) {
            deferred.resolve({ total_replies: 0 });
        } else {
            deferred.reject(rv.body);
        }
    });
    return deferred.promise;
};

var count = function (urls) {
    var deferred = Q.defer();
    curl("POST", endpoint + "/count", JSON.stringify(urls), function (rv) {
        if (rv.status === 200) {
            deferred.resolve(JSON.parse(rv.body));
        } else {
            deferred.reject(rv.body);
        }
    });
    return deferred.promise;
};

var like = function (id) {
    var deferred = Q.defer();
    curl("POST", endpoint + "/id/" + id + "/like", null, function (rv) {
        deferred.resolve(JSON.parse(rv.body));
    });
    return deferred.promise;
};

var dislike = function (id) {
    var deferred = Q.defer();
    curl("POST", endpoint + "/id/" + id + "/dislike", null, function (rv) {
        deferred.resolve(JSON.parse(rv.body));
    });
    return deferred.promise;
};

var feed = function (tid) {
    return endpoint + "/feed?" + qs({ uri: tid || location() });
};

var preview = function (text) {
    var deferred = Q.defer();
    curl(
        "POST",
        endpoint + "/preview",
        JSON.stringify({ text: text }),
        function (rv) {
            if (rv.status === 200) {
                deferred.resolve(JSON.parse(rv.body).text);
            } else {
                deferred.reject(rv.body);
            }
        }
    );
    return deferred.promise;
};

module.exports = {
    endpoint: endpoint,
    salt: salt,
    create: create,
    modify: modify,
    remove: remove,
    view: view,
    fetch: fetch,
    count: count,
    like: like,
    dislike: dislike,
    feed: feed,
    preview: preview,
};


/***/ }),

/***/ "./nikas/js/app/config.js":
/*!********************************!*\
  !*** ./nikas/js/app/config.js ***!
  \********************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

var utils = __webpack_require__(/*! app/utils */ "./nikas/js/app/utils.js");

("use strict");

var config = {
    css: true,
    "css-url": null,
    lang: "",
    "default-lang": "fa",
    "reply-to-self": false,
    "require-email": false,
    "require-author": false,
    "reply-notifications": false,
    "max-comments-top": "inf",
    "max-comments-nested": 5,
    "reveal-on-click": 5,
    gravatar: false,
    avatar: true,
    "avatar-bg": "#f0f0f0",
    "avatar-fg": [
        "#9abf88",
        "#5698c4",
        "#e279a3",
        "#9163b6",
        "#be5168",
        "#f19670",
        "#e4bf80",
        "#447c69",
    ].join(" "),
    vote: true,
    "vote-levels": null,
    feed: false,
};

var js = document.getElementsByTagName("script");

for (var i = 0; i < js.length; i++) {
    for (var j = 0; j < js[i].attributes.length; j++) {
        var attr = js[i].attributes[j];
        if (/^data-nikas-/.test(attr.name)) {
            try {
                config[attr.name.substring(10)] = JSON.parse(attr.value);
            } catch (ex) {
                config[attr.name.substring(10)] = attr.value;
            }
        }
    }
}

// split avatar-fg on whitespace
config["avatar-fg"] = config["avatar-fg"].split(" ");

// create an array of normalized language codes from:
//   - config["lang"], if it is nonempty
//   - the first of navigator.languages, navigator.language, and
//     navigator.userLanguage that exists and has a nonempty value
//   - config["default-lang"]
//   - "en" as an ultimate fallback
// i18n.js will use the first code in this array for which we have
// a translation.
var languages = [];
var found_navlang = false;
if (config["lang"]) {
    languages.push(utils.normalize_bcp47(config["lang"]));
}
if (navigator.languages) {
    for (i = 0; i < navigator.languages.length; i++) {
        if (navigator.languages[i]) {
            found_navlang = true;
            languages.push(utils.normalize_bcp47(navigator.languages[i]));
        }
    }
}
if (!found_navlang && navigator.language) {
    found_navlang = true;
    languages.push(utils.normalize_bcp47(navigator.language));
}
if (!found_navlang && navigator.userLanguage) {
    found_navlang = true;
    languages.push(utils.normalize_bcp47(navigator.userLanguage));
}
if (config["default-lang"]) {
    languages.push(utils.normalize_bcp47(config["default-lang"]));
}
languages.push("fa");

config["langs"] = languages;
// code outside this file should look only at langs
delete config["lang"];
delete config["default-lang"];

module.exports = config;


/***/ }),

/***/ "./nikas/js/app/count.js":
/*!*******************************!*\
  !*** ./nikas/js/app/count.js ***!
  \*******************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

var api = __webpack_require__(/*! app/api */ "./nikas/js/app/api.js");
var $ = __webpack_require__(/*! app/dom */ "./nikas/js/app/dom.js");
var i18n = __webpack_require__(/*! app/i18n */ "./nikas/js/app/i18n.js");

module.exports = function () {
    var objs = {};

    $.each("a", function (el) {
        if (!el.href.match || !el.href.match(/#nikas-thread$/)) {
            return;
        }

        var tid =
            el.getAttribute("data-nikas-id") ||
            el.href
                .match(/^(.+)#nikas-thread$/)[1]
                .replace(/^.*\/\/[^\/]+/, "");

        if (tid in objs) {
            objs[tid].push(el);
        } else {
            objs[tid] = [el];
        }
    });

    var urls = Object.keys(objs);

    api.count(urls).then(function (rv) {
        for (var key in objs) {
            if (objs.hasOwnProperty(key)) {
                var index = urls.indexOf(key);

                for (var i = 0; i < objs[key].length; i++) {
                    objs[key][i].textContent = i18n.pluralize(
                        "num-comments",
                        rv[index]
                    );
                }
            }
        }
    });
};


/***/ }),

/***/ "./nikas/js/app/dom.js":
/*!*****************************!*\
  !*** ./nikas/js/app/dom.js ***!
  \*****************************/
/***/ (function(module) {

"use strict";


function Element(node) {
    this.obj = node;

    this.replace = function (el) {
        var element = DOM.htmlify(el);
        node.parentNode.replaceChild(element.obj, node);
        return element;
    };

    this.prepend = function (el) {
        var element = DOM.htmlify(el);
        node.insertBefore(element.obj, node.firstChild);
        return element;
    };

    this.append = function (el) {
        var element = DOM.htmlify(el);
        node.appendChild(element.obj);
        return element;
    };

    this.insertAfter = function (el) {
        var element = DOM.htmlify(el);
        node.parentNode.insertBefore(element.obj, node.nextSibling);
        return element;
    };

    /**
     * Shortcut for `Element.addEventListener`, prevents default event
     * by default, set :param prevents: to `false` to change that behavior.
     */
    this.on = function (type, listener, prevent) {
        node.addEventListener(type, function (event) {
            listener(event);
            if (prevent === undefined || prevent) {
                event.preventDefault();
            }
        });
    };

    /**
     * Toggle between two internal states on event :param type: e.g. to
     * cycle form visibility. Callback :param a: is called on first event,
     * :param b: next time.
     *
     * You can skip to the next state without executing the callback with
     * `toggler.next()`. You can prevent a cycle when you call `toggler.wait()`
     * during an event.
     */
    this.toggle = function (type, a, b) {
        var toggler = new Toggle(a, b);
        this.on(type, function () {
            toggler.next();
        });
    };

    this.detach = function () {
        // Detach an element from the DOM and return it.
        node.parentNode.removeChild(this.obj);
        return this;
    };

    this.remove = function () {
        // IE quirks
        node.parentNode.removeChild(this.obj);
    };

    this.show = function () {
        node.style.display = "block";
    };

    this.hide = function () {
        node.style.display = "none";
    };

    this.setText = function (text) {
        node.textContent = text;
    };

    this.setHtml = function (html) {
        node.innerHTML = html;
    };

    this.blur = function () {
        node.blur();
    };
    this.focus = function () {
        node.focus();
    };
    this.scrollIntoView = function (args) {
        node.scrollIntoView(args);
    };

    this.checked = function () {
        return node.checked;
    };

    this.setAttribute = function (key, value) {
        node.setAttribute(key, value);
    };
    this.getAttribute = function (key) {
        return node.getAttribute(key);
    };

    this.classList = node.classList;

    Object.defineProperties(this, {
        textContent: {
            get: function () {
                return node.textContent;
            },
            set: function (textContent) {
                node.textContent = textContent;
            },
        },
        innerHTML: {
            get: function () {
                return node.innerHTML;
            },
            set: function (innerHTML) {
                node.innerHTML = innerHTML;
            },
        },
        value: {
            get: function () {
                return node.value;
            },
            set: function (value) {
                node.value = value;
            },
        },
        placeholder: {
            get: function () {
                return node.placeholder;
            },
            set: function (placeholder) {
                node.placeholder = placeholder;
            },
        },
    });
}

var Toggle = function (a, b) {
    this.state = false;

    this.next = function () {
        if (!this.state) {
            this.state = true;
            a(this);
        } else {
            this.state = false;
            b(this);
        }
    };

    this.wait = function () {
        this.state = !this.state;
    };
};

var DOM = function (query, root, single) {
    /*
    jQuery-like CSS selector which returns on :param query: either a
    single node (unless single=false), a node list or null.

    :param root: only queries within the given element.
     */

    if (typeof single === "undefined") {
        single = true;
    }

    if (!root) {
        root = window.document;
    }

    if (root instanceof Element) {
        root = root.obj;
    }
    var elements = [].slice.call(root.querySelectorAll(query), 0);

    if (elements.length === 0) {
        return null;
    }

    if (elements.length === 1 && single) {
        return new Element(elements[0]);
    }

    // convert NodeList to Array
    elements = [].slice.call(elements, 0);

    return elements.map(function (el) {
        return new Element(el);
    });
};

DOM.htmlify = function (el) {
    /*
    Convert :param html: into an Element (if not already).
    */

    if (el instanceof Element) {
        return el;
    }

    if (el instanceof window.Element) {
        return new Element(el);
    }

    var wrapper = DOM.new("div");
    wrapper.innerHTML = el;
    return new Element(wrapper.firstChild);
};

DOM.new = function (tag, content) {
    /*
    A helper to build HTML with pure JS. You can pass class names and
    default content as well:

        var par = DOM.new("p"),
            div = DOM.new("p.some.classes"),
            div = DOM.new("textarea.foo", "...")
     */

    var el = document.createElement(tag.split(".")[0]);
    tag.split(".")
        .slice(1)
        .forEach(function (val) {
            el.classList.add(val);
        });

    if (["A", "LINK"].indexOf(el.nodeName) > -1) {
        el.href = "#";
    }

    if (!content && content !== 0) {
        content = "";
    }
    if (["TEXTAREA", "INPUT"].indexOf(el.nodeName) > -1) {
        el.value = content;
    } else {
        el.textContent = content;
    }
    return el;
};

DOM.each = function (tag, func) {
    // XXX really needed? Maybe better as NodeList method
    Array.prototype.forEach.call(document.getElementsByTagName(tag), func);
};

module.exports = DOM;


/***/ }),

/***/ "./nikas/js/app/globals.js":
/*!*********************************!*\
  !*** ./nikas/js/app/globals.js ***!
  \*********************************/
/***/ (function(module) {

"use strict";


var Offset = function () {
    this.values = [];
};

Offset.prototype.update = function (remoteTime) {
    this.values.push(new Date().getTime() - remoteTime.getTime());
};

Offset.prototype.localTime = function () {
    return new Date(
        new Date().getTime() -
            this.values.reduce(function (a, b) {
                return a + b;
            }) /
                this.values.length
    );
};

var offset = new Offset();

module.exports = {
    offset: offset,
};


/***/ }),

/***/ "./nikas/js/app/i18n.js":
/*!******************************!*\
  !*** ./nikas/js/app/i18n.js ***!
  \******************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

var config = __webpack_require__(/*! app/config */ "./nikas/js/app/config.js");

var fa = __webpack_require__(/*! app/i18n/fa */ "./nikas/js/app/i18n/fa.js");

("use strict");

var pluralforms = function (_lang) {
    return function (msgs, n) {
        return msgs[n === 1 ? 0 : 1];
    };
};

var catalogue = {
    fa: fa,
};

// for each entry in config.langs, see whether we have a catalogue
// entry and a pluralforms entry for it.  if we don't, try chopping
// off everything but the primary language subtag, before moving
// on to the next one.
var lang, plural, translations;
for (let value of config.langs) {
    lang = value;
    plural = pluralforms(lang);
    translations = catalogue[lang];
    if (plural && translations) break;
    if (/-/.test(lang)) {
        lang = lang.split("-", 1)[0];
        plural = pluralforms(lang);
        translations = catalogue[lang];
        if (plural && translations) break;
    }
}

// absolute backstop; if we get here there's a bug in config.js
if (!plural || !translations) {
    lang = "fa";
    plural = pluralforms(lang);
    translations = catalogue[lang];
}

var translate = function (msgid) {
    return (
        config[msgid + "-text-" + lang] ||
        translations[msgid] ||
        en[msgid] ||
        "[?" + msgid + "]"
    );
};

var pluralize = function (msgid, n) {
    var msg;

    msg = translate(msgid);
    if (msg.indexOf("\n") > -1) {
        msg = plural(msg.split("\n"), +n);
    }

    return msg ? msg.replace("{{ n }}", +n) : msg;
};

var ago = function (localTime, date) {
    var secs = (localTime.getTime() - date.getTime()) / 1000;

    if (isNaN(secs) || secs < 0) {
        secs = 0;
    }

    var mins = Math.floor(secs / 60),
        hours = Math.floor(mins / 60),
        days = Math.floor(hours / 24);

    return (
        (secs <= 45 && translate("date-now")) ||
        (secs <= 90 && pluralize("date-minute", 1)) ||
        (mins <= 45 && pluralize("date-minute", mins)) ||
        (mins <= 90 && pluralize("date-hour", 1)) ||
        (hours <= 22 && pluralize("date-hour", hours)) ||
        (hours <= 36 && pluralize("date-day", 1)) ||
        (days <= 5 && pluralize("date-day", days)) ||
        (days <= 8 && pluralize("date-week", 1)) ||
        (days <= 21 && pluralize("date-week", Math.floor(days / 7))) ||
        (days <= 45 && pluralize("date-month", 1)) ||
        (days <= 345 && pluralize("date-month", Math.floor(days / 30))) ||
        (days <= 547 && pluralize("date-year", 1)) ||
        pluralize("date-year", Math.floor(days / 365.25))
    );
};

module.exports = {
    ago: ago,
    lang: lang,
    translate: translate,
    pluralize: pluralize,
};


/***/ }),

/***/ "./nikas/js/app/i18n/fa.js":
/*!*********************************!*\
  !*** ./nikas/js/app/i18n/fa.js ***!
  \*********************************/
/***/ (function(module) {

module.exports = {
    "postbox-text": "متن نظر را اینجا وارد کنید - حداقل ۳ حرف",
    "postbox-author": "نام (اختیاری)",
    "postbox-email": "آدرس ایمیل (اختیاری)",
    "postbox-website": "آدرس وب سایت (اختیاری)",
    "postbox-preview": "پیش نمایش",
    "postbox-edit": "ویرایش",
    "postbox-submit": "ثبت",
    "postbox-notification": "اطلاع رسانی از طریق ایمیل",

    "num-comments": "یک نظر\n{{ n }} نظر",
    "no-comments": "هنوز نظری ثبت نشده است",
    "atom-feed": "فید اتم",

    "comment-reply": "پاسخ",
    "comment-edit": "ویرایش",
    "comment-save": "ذخیره",
    "comment-delete": "حذف",
    "comment-confirm": "تایید",
    "comment-close": "بستن",
    "comment-cancel": "لغو",
    "comment-deleted": "نظر حذف شد",
    "comment-queued": "در انتظار بررسی توسط مدیریت",
    "comment-anonymous": "ناشناس",
    "comment-hidden": "{{ n }} مخفی",

    "date-now": "همین الان",
    "date-minute": "یک دقیقه پیش\n{{ n }} دقیقه پیش",
    "date-hour": "یک ساعت پیش\n{{ n }} ساعت پیش",
    "date-day": "دیروز\n{{ n }} روز پیش",
    "date-week": "هفته پیش\n{{ n }} هفته پیش",
    "date-month": "ماه پیش\n{{ n }} ماه پیش",
    "date-year": "سال پیش\n{{ n }} سال پیش",
};


/***/ }),

/***/ "./nikas/js/app/lib/identicons.js":
/*!****************************************!*\
  !*** ./nikas/js/app/lib/identicons.js ***!
  \****************************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

var Q = __webpack_require__(/*! app/lib/promise */ "./nikas/js/app/lib/promise.js");

("use strict");

// Number of squares width and height
var GRID = 5;

var pad = function (n, width) {
    return n.length >= width
        ? n
        : new Array(width - n.length + 1).join("0") + n;
};

/**
 * Fill in a square on the canvas.
 */
var fill = function (svg, x, y, padding, size, color) {
    var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");

    rect.setAttribute("x", padding + x * size);
    rect.setAttribute("y", padding + y * size);
    rect.setAttribute("width", size);
    rect.setAttribute("height", size);
    rect.setAttribute("style", "fill: " + color);

    svg.appendChild(rect);
};

/**
 * Pick random squares to fill in.
 */
var generateIdenticon = function (key, padding, size, config) {
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("version", "1.1");
    svg.setAttribute("viewBox", "0 0 " + size + " " + size);
    svg.setAttribute("preserveAspectRatio", "xMinYMin meet");
    svg.setAttribute("shape-rendering", "crispEdges");
    fill(svg, 0, 0, 0, size + 2 * padding, config["avatar-bg"]);

    if (typeof key === null) {
        return svg;
    }

    Q.when(key, function (key) {
        var hash = pad(
                (parseInt(key.substr(-16), 16) % Math.pow(2, 18)).toString(2),
                18
            ),
            index = 0;

        svg.setAttribute("data-hash", key);

        var i = parseInt(hash.substring(hash.length - 3, hash.length), 2),
            color = config["avatar-fg"][i % config["avatar-fg"].length];

        for (var x = 0; x < Math.ceil(GRID / 2); x++) {
            for (var y = 0; y < GRID; y++) {
                if (hash.charAt(index) === "1") {
                    fill(svg, x, y, padding, 8, color);

                    // fill right sight symmetrically
                    if (x < Math.floor(GRID / 2)) {
                        fill(svg, GRID - 1 - x, y, padding, 8, color);
                    }
                }
                index++;
            }
        }
    });

    return svg;
};

/* TODO: This function is currently unused and should be removed */
var generateBlank = function (height, width, config) {
    var blank = parseInt(
        [
            0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, /* purple: */ 0, 1, 0,
        ].join(""),
        2
    ).toString(16);

    var el = generateIdenticon(blank, height, width, config);
    el.setAttribute("className", "blank"); // IE10 does not support classList on SVG elements, duh.

    return el;
};

module.exports = {
    generate: generateIdenticon,
    blank: generateBlank,
};


/***/ }),

/***/ "./nikas/js/app/lib/promise.js":
/*!*************************************!*\
  !*** ./nikas/js/app/lib/promise.js ***!
  \*************************************/
/***/ (function(module) {

"use strict";


var stderr = function (text) {
    console.log(text);
};

var Promise = function () {
    this.success = [];
    this.errors = [];
};

Promise.prototype.then = function (onSuccess, onError) {
    this.success.push(onSuccess);
    if (onError) {
        this.errors.push(onError);
    } else {
        this.errors.push(stderr);
    }
};

var Defer = function () {
    this.promise = new Promise();
};

Defer.prototype = {
    promise: Promise,
    resolve: function (rv) {
        this.promise.success.forEach(function (callback) {
            window.setTimeout(function () {
                callback(rv);
            }, 0);
        });
    },

    reject: function (error) {
        this.promise.errors.forEach(function (callback) {
            window.setTimeout(function () {
                callback(error);
            }, 0);
        });
    },
};

var when = function (obj, func) {
    if (obj instanceof Promise) {
        return obj.then(func);
    } else {
        return func(obj);
    }
};

var defer = function () {
    return new Defer();
};

module.exports = {
    defer: defer,
    when: when,
};


/***/ }),

/***/ "./nikas/js/app/lib/ready.js":
/*!***********************************!*\
  !*** ./nikas/js/app/lib/ready.js ***!
  \***********************************/
/***/ (function(module) {

"use strict";


var loaded = false;
var once = function (callback) {
    if (!loaded) {
        loaded = true;
        callback();
    }
};

var domready = function (callback) {
    // HTML5 standard to listen for dom readiness
    document.addEventListener("DOMContentLoaded", function () {
        once(callback);
    });

    // if dom is already ready, just run callback
    if (
        document.readyState === "interactive" ||
        document.readyState === "complete"
    ) {
        once(callback);
    }
};

module.exports = domready;


/***/ }),

/***/ "./nikas/js/app/nikas.js":
/*!*******************************!*\
  !*** ./nikas/js/app/nikas.js ***!
  \*******************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

var $ = __webpack_require__(/*! app/dom */ "./nikas/js/app/dom.js");
var utils = __webpack_require__(/*! app/utils */ "./nikas/js/app/utils.js");
var config = __webpack_require__(/*! app/config */ "./nikas/js/app/config.js");
var api = __webpack_require__(/*! app/api */ "./nikas/js/app/api.js");
var template = __webpack_require__(/*! app/template */ "./nikas/js/app/template.js");
var i18n = __webpack_require__(/*! app/i18n */ "./nikas/js/app/i18n.js");
var identicons = __webpack_require__(/*! app/lib/identicons */ "./nikas/js/app/lib/identicons.js");
var globals = __webpack_require__(/*! app/globals */ "./nikas/js/app/globals.js");

("use strict");

var editorify = function (el) {
    el = $.htmlify(el);
    el.setAttribute("contentEditable", true);

    el.on("focus", function () {
        if (el.classList.contains("nikas-placeholder")) {
            el.innerHTML = "";
            el.classList.remove("nikas-placeholder");
        }
    });

    el.on("blur", function () {
        if (el.textContent.length === 0) {
            el.textContent = i18n.translate("postbox-text");
            el.classList.add("nikas-placeholder");
        }
    });

    return el;
};

var Postbox = function (parent) {
    var localStorage = utils.localStorageImpl,
        el = $.htmlify(
            template.render("postbox", {
                author: JSON.parse(localStorage.getItem("nikas-author")),
                email: JSON.parse(localStorage.getItem("nikas-email")),
                website: JSON.parse(localStorage.getItem("nikas-website")),
                preview: "",
            })
        );

    // callback on success (e.g. to toggle the reply button)
    el.onsuccess = function () {};

    el.validate = function () {
        if (
            utils.text($(".nikas-textarea", this).innerHTML).length < 3 ||
            $(".nikas-textarea", this).classList.contains("nikas-placeholder")
        ) {
            $(".nikas-textarea", this).focus();
            return false;
        }
        if (
            config["require-email"] &&
            $("[name='email']", this).value.length <= 0
        ) {
            $("[name='email']", this).focus();
            return false;
        }
        if (
            config["require-author"] &&
            $("[name='author']", this).value.length <= 0
        ) {
            $("[name='author']", this).focus();
            return false;
        }
        return true;
    };

    // only display notification checkbox if email is filled in
    var email_edit = function () {
        if (
            config["reply-notifications"] &&
            $("[name='email']", el).value.length > 0
        ) {
            $(".nikas-notification-section", el).show();
        } else {
            $(".nikas-notification-section", el).hide();
        }
    };
    $("[name='email']", el).on("input", email_edit);
    email_edit();

    // email is not optional if this config parameter is set
    if (config["require-email"]) {
        $("[name='email']", el).setAttribute(
            "placeholder",
            $("[name='email']", el)
                .getAttribute("placeholder")
                .replace(/ \(.*\)/, "")
        );
    }

    // author is not optional if this config parameter is set
    if (config["require-author"]) {
        $("[name='author']", el).placeholder = $(
            "[name='author']",
            el
        ).placeholder.replace(/ \(.*\)/, "");
    }

    // preview function
    $("[name='preview']", el).on("click", function () {
        api.preview(utils.text($(".nikas-textarea", el).innerHTML)).then(
            function (html) {
                $(".preview .text", el).innerHTML = html;
                el.classList.add("nikas-preview-mode");
            }
        );
    });

    // edit function
    var edit = function () {
        $(".nikas-preview .nikas-text", el).innerHTML = "";
        el.classList.remove("nikas-preview-mode");
    };
    $("[name='edit']", el).on("click", edit);
    $(".nikas-preview", el).on("click", edit);

    // submit form, initialize optional fields with `null` and reset form.
    // If replied to a comment, remove form completely.
    $("[type=submit]", el).on("click", function () {
        edit();
        if (!el.validate()) {
            return;
        }

        var author = $("[name=author]", el).value || null,
            email = $("[name=email]", el).value || null,
            website = $("[name=website]", el).value || null;

        localStorage.setItem("nikas-author", JSON.stringify(author));
        localStorage.setItem("nikas-email", JSON.stringify(email));
        localStorage.setItem("nikas-website", JSON.stringify(website));

        api.create($("#nikas-thread").getAttribute("data-nikas-id"), {
            author: author,
            email: email,
            website: website,
            text: utils.text($(".nikas-textarea", el).innerHTML),
            parent: parent || null,
            title: $("#nikas-thread").getAttribute("data-title") || null,
            notification: $("[name=notification]", el).checked() ? 1 : 0,
        }).then(function (comment) {
            $(".nikas-textarea", el).innerHTML = "";
            $(".nikas-textarea", el).blur();
            insert(comment, true);

            if (parent !== null) {
                el.onsuccess();
            }
        });
    });

    editorify($(".nikas-textarea", el));

    return el;
};

var insert_loader = function (comment, lastcreated) {
    var entrypoint;
    if (comment.id === null) {
        entrypoint = $("#nikas-root");
        comment.name = "null";
    } else {
        entrypoint = $(
            "#nikas-" + comment.id + " > .nikas-text-wrapper > .nikas-follow-up"
        );
        comment.name = comment.id;
    }
    var el = $.htmlify(template.render("comment-loader", { comment: comment }));

    entrypoint.append(el);

    $("a.nikas-load-hidden", el).on("click", function () {
        el.remove();
        api.fetch(
            $("#nikas-thread").getAttribute("data-nikas-id"),
            config["reveal-on-click"],
            config["max-comments-nested"],
            comment.id,
            lastcreated
        ).then(
            function (rv) {
                if (rv.total_replies === 0) {
                    return;
                }

                var lastcreated = 0;
                rv.replies.forEach(function (commentObject) {
                    insert(commentObject, false);
                    if (commentObject.created > lastcreated) {
                        lastcreated = commentObject.created;
                    }
                });

                if (rv.hidden_replies > 0) {
                    insert_loader(rv, lastcreated);
                }
            },
            function (err) {
                console.log(err);
            }
        );
    });
};

var insert = function (comment, scrollIntoView) {
    var el = $.htmlify(template.render("comment", { comment: comment }));

    // update datetime every 60 seconds
    var refresh = function () {
        $(".nikas-permalink > time", el).textContent = i18n.ago(
            globals.offset.localTime(),
            new Date(parseInt(comment.created, 10) * 1000)
        );
        setTimeout(refresh, 60 * 1000);
    };

    // run once to activate
    refresh();

    if (config["avatar"]) {
        $(".nikas-avatar > svg", el).replace(
            identicons.generate(comment.hash, 4, 48, config)
        );
    }

    var entrypoint;
    if (comment.parent === null) {
        entrypoint = $("#nikas-root");
    } else {
        entrypoint = $(
            "#nikas-" +
                comment.parent +
                " > .nikas-text-wrapper > .nikas-follow-up"
        );
    }

    entrypoint.append(el);

    if (scrollIntoView) {
        el.scrollIntoView();
    }

    var footer = $(
            "#nikas-" +
                comment.id +
                " > .nikas-text-wrapper > .nikas-comment-footer"
        ),
        header = $(
            "#nikas-" +
                comment.id +
                " > .nikas-text-wrapper > .nikas-comment-header"
        ),
        text = $(
            "#nikas-" + comment.id + " > .nikas-text-wrapper > .nikas-text"
        );

    var form = null; // XXX: probably a good place for a closure
    $("a.nikas-reply", footer).toggle(
        "click",
        function (toggler) {
            form = footer.insertAfter(
                new Postbox(
                    comment.parent === null ? comment.id : comment.parent
                )
            );
            form.onsuccess = function () {
                toggler.next();
            };
            $(".nikas-textarea", form).focus();
            $("a.nikas-reply", footer).textContent =
                i18n.translate("comment-close");
        },
        function () {
            form.remove();
            $("a.nikas-reply", footer).textContent =
                i18n.translate("comment-reply");
        }
    );

    if (config.vote) {
        var voteLevels = config["vote-levels"];
        if (typeof voteLevels === "string") {
            // Eg. -5,5,15
            voteLevels = voteLevels.split(",");
        }

        // update vote counter
        var votes = function (value) {
            var span = $("span.nikas-votes", footer);
            if (span === null) {
                footer.prepend($.new("span.nikas-votes", value));
            } else {
                span.textContent = value;
            }
            if (value) {
                el.classList.remove("nikas-no-votes");
            } else {
                el.classList.add("nikas-no-votes");
            }
            if (voteLevels) {
                var before = true;
                for (var index = 0; index <= voteLevels.length; index++) {
                    if (
                        before &&
                        (index >= voteLevels.length ||
                            value < voteLevels[index])
                    ) {
                        el.classList.add("nikas-vote-level-" + index);
                        before = false;
                    } else {
                        el.classList.remove("nikas-vote-level-" + index);
                    }
                }
            }
        };

        $("a.nikas-upvote", footer).on("click", function () {
            api.like(comment.id).then(function (rv) {
                votes(rv.likes - rv.dislikes);
            });
        });

        $("a.nikas-downvote", footer).on("click", function () {
            api.dislike(comment.id).then(function (rv) {
                votes(rv.likes - rv.dislikes);
            });
        });

        votes(comment.likes - comment.dislikes);
    }

    $("a.nikas-edit", footer).toggle(
        "click",
        function (toggler) {
            var edit = $("a.nikas-edit", footer);
            var avatar =
                config["avatar"] || config["gravatar"]
                    ? $(".nikas-avatar", el, false)[0]
                    : null;

            edit.textContent = i18n.translate("comment-save");
            edit.insertAfter(
                $.new("a.nikas-cancel", i18n.translate("comment-cancel"))
            ).on("click", function () {
                toggler.canceled = true;
                toggler.next();
            });

            toggler.canceled = false;
            api.view(comment.id, 1).then(function (rv) {
                var textarea = editorify($.new("div.nikas-textarea"));

                textarea.innerHTML = utils.detext(rv.text);
                textarea.focus();

                text.classList.remove("nikas-text");
                text.classList.add("nikas-textarea-wrapper");

                text.textContent = "";
                text.append(textarea);
            });

            if (avatar !== null) {
                avatar.hide();
            }
        },
        function (toggler) {
            var textarea = $(".nikas-textarea", text);
            var avatar =
                config["avatar"] || config["gravatar"]
                    ? $(".nikas-avatar", el, false)[0]
                    : null;

            if (!toggler.canceled && textarea !== null) {
                if (utils.text(textarea.innerHTML).length < 3) {
                    textarea.focus();
                    toggler.wait();
                    return;
                } else {
                    api.modify(comment.id, {
                        text: utils.text(textarea.innerHTML),
                    }).then(function (rv) {
                        text.innerHTML = rv.text;
                        comment.text = rv.text;
                    });
                }
            } else {
                text.innerHTML = comment.text;
            }

            text.classList.remove("nikas-textarea-wrapper");
            text.classList.add("nikas-text");

            if (avatar !== null) {
                avatar.show();
            }

            $("a.nikas-cancel", footer).remove();
            $("a.nikas-edit", footer).textContent =
                i18n.translate("comment-edit");
        }
    );

    $("a.nikas-delete", footer).toggle(
        "click",
        function (toggler) {
            var del = $("a.nikas-delete", footer);
            var state = !toggler.state;

            del.textContent = i18n.translate("comment-confirm");
            del.on("mouseout", function () {
                del.textContent = i18n.translate("comment-delete");
                toggler.state = state;
                del.onmouseout = null;
            });
        },
        function () {
            var del = $("a.nikas-delete", footer);
            api.remove(comment.id).then(function (rv) {
                if (rv) {
                    el.remove();
                } else {
                    $("span.nikas-note", header).textContent =
                        i18n.translate("comment-deleted");
                    text.innerHTML = "<p>&nbsp;</p>";
                    $("a.nikas-edit", footer).remove();
                    $("a.nikas-delete", footer).remove();
                }
                del.textContent = i18n.translate("comment-delete");
            });
        }
    );

    // remove edit and delete buttons when cookie is gone
    var clear = function (button) {
        if (!utils.cookie("nikas-" + comment.id)) {
            if ($(button, footer) !== null) {
                $(button, footer).remove();
            }
        } else {
            setTimeout(function () {
                clear(button);
            }, 15 * 1000);
        }
    };

    clear("a.nikas-edit");
    clear("a.nikas-delete");

    // show direct reply to own comment when cookie is max aged
    var show = function (el) {
        if (utils.cookie("nikas-" + comment.id)) {
            setTimeout(function () {
                show(el);
            }, 15 * 1000);
        } else {
            footer.append(el);
        }
    };

    if (!config["reply-to-self"] && utils.cookie("nikas-" + comment.id)) {
        show($("a.nikas-reply", footer).detach());
    }

    if (comment.hasOwnProperty("replies")) {
        var lastcreated = 0;
        comment.replies.forEach(function (replyObject) {
            insert(replyObject, false);
            if (replyObject.created > lastcreated) {
                lastcreated = replyObject.created;
            }
        });
        if (comment.hidden_replies > 0) {
            insert_loader(comment, lastcreated);
        }
    }
};

module.exports = {
    insert: insert,
    insert_loader: insert_loader,
    Postbox: Postbox,
};


/***/ }),

/***/ "./nikas/js/app/svg.js":
/*!*****************************!*\
  !*** ./nikas/js/app/svg.js ***!
  \*****************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

module.exports = {
    "arrow-down": __webpack_require__(/*! app/svg/arrow-down.svg */ "./nikas/js/app/svg/arrow-down.svg"),
    "arrow-up": __webpack_require__(/*! app/svg/arrow-up.svg */ "./nikas/js/app/svg/arrow-up.svg"),
};


/***/ }),

/***/ "./nikas/js/app/template.js":
/*!**********************************!*\
  !*** ./nikas/js/app/template.js ***!
  \**********************************/
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

var utils = __webpack_require__(/*! app/utils */ "./nikas/js/app/utils.js");

var tmpl_postbox = __webpack_require__(/*! app/templates/postbox */ "./nikas/js/app/templates/postbox.js");
var tmpl_comment = __webpack_require__(/*! app/templates/comment */ "./nikas/js/app/templates/comment.js");
var tmpl_comment_loader = __webpack_require__(/*! app/templates/comment-loader */ "./nikas/js/app/templates/comment-loader.js");

("use strict");

var globals = {},
    templates = {};

var load_tmpl = function (name, tmpl) {
    templates[name] = tmpl;
};

var set = function (name, value) {
    globals[name] = value;
};

load_tmpl("postbox", tmpl_postbox);
load_tmpl("comment", tmpl_comment);
load_tmpl("comment-loader", tmpl_comment_loader);

set("bool", function (arg) {
    return arg ? true : false;
});
set("humanize", function (date) {
    if (typeof date !== "object") {
        date = new Date(parseInt(date, 10) * 1000);
    }

    return date.toString();
});
set("datetime", function (date) {
    if (typeof date !== "object") {
        date = new Date(parseInt(date, 10) * 1000);
    }

    return (
        [
            date.getUTCFullYear(),
            utils.pad(date.getUTCMonth(), 2),
            utils.pad(date.getUTCDay(), 2),
        ].join("-") +
        "T" +
        [
            utils.pad(date.getUTCHours(), 2),
            utils.pad(date.getUTCMinutes(), 2),
            utils.pad(date.getUTCSeconds(), 2),
        ].join(":") +
        "Z"
    );
});

var render = function (name, locals) {
    var rv,
        t = templates[name];
    if (!t) {
        throw new Error("Template not found: '" + name + "'");
    }

    locals = locals || {};

    var keys = [];
    for (var key in locals) {
        if (locals.hasOwnProperty(key) && !globals.hasOwnProperty(key)) {
            keys.push(key);
            globals[key] = locals[key];
        }
    }

    rv = templates[name](globals);

    // These are all needed, else DOM.htmlify will fail to create the element!
    // Strip newlines rendered from template literals
    rv = rv.replace(/\r?\n|\r/g, " ");
    // Trim whitespace
    rv = rv.trim();

    for (let value of keys) {
        delete globals[value];
    }

    return rv;
};

module.exports = {
    set: set,
    render: render,
};


/***/ }),

/***/ "./nikas/js/app/templates/comment-loader.js":
/*!**************************************************!*\
  !*** ./nikas/js/app/templates/comment-loader.js ***!
  \**************************************************/
/***/ (function(module) {

var html = function (globals) {
    var comment = globals.comment;
    var pluralize = globals.pluralize;

    return (
        "" +
        "<div class='nikas-comment-loader' id='nikas-loader-" +
        comment.name +
        "'>" +
        "<a class='nikas-load-hidden' href='#'>" +
        pluralize("comment-hidden", comment.hidden_replies) +
        "</a>" +
        "</div>"
    );
};
module.exports = html;


/***/ }),

/***/ "./nikas/js/app/templates/comment.js":
/*!*******************************************!*\
  !*** ./nikas/js/app/templates/comment.js ***!
  \*******************************************/
/***/ (function(module) {

var html = function (globals) {
    var i18n = globals.i18n;
    var comment = globals.comment;
    var conf = globals.conf;
    var datetime = globals.datetime;
    var humanize = globals.humanize;
    var svg = globals.svg;

    var author = comment.author ? comment.author : i18n("comment-anonymous");

    return (
        "" +
        "<div class='nikas-comment' id='nikas-" +
        comment.id +
        "'>" +
        (conf.gravatar
            ? "<div class='nikas-avatar'><img src='" +
              comment.gravatar_image +
              "'></div>"
            : "") +
        (conf.avatar
            ? "<div class='nikas-avatar'><svg data-hash='" +
              comment.hash +
              "'</svg></div>"
            : "") +
        "<div class='nikas-text-wrapper'>" +
        "<div class='nikas-comment-header' role='meta'>" +
        (comment.website
            ? "<a class='nikas-author' href='" +
              comment.website +
              "' rel='nofollow'>" +
              author +
              "</a>"
            : "<span class='nikas-author'>" + author + "</span>") +
        "<span class='nikas-spacer'>&bull;</span>" +
        "<a class='nikas-permalink' href='#nikas-" +
        comment.id +
        "'>" +
        "<time title='" +
        humanize(comment.created) +
        "' datetime='" +
        datetime(comment.created) +
        "'>" +
        humanize(comment.created) +
        "</time>" +
        "</a>" +
        "<span class='nikas-note'>" +
        (comment.mode == 2
            ? i18n("comment-queued")
            : comment.mode == 4
            ? i18n("comment-deleted")
            : "") +
        "</span>" +
        "</div>" + // .text-wrapper
        "<div class='nikas-text'>" +
        (comment.mode == 4 ? "<p>&nbsp;</p>" : comment.text) +
        "</div>" + // .text
        "<div class='nikas-comment-footer'>" +
        (conf.vote
            ? "<a class='nikas-upvote' href='#'>" +
              svg["arrow-up"] +
              "</a>" +
              "<span class='nikas-spacer'>|</span>" +
              "<a class='nikas-downvote' href='#'>" +
              svg["arrow-down"] +
              "</a>"
            : "") +
        "<a class='nikas-reply' href='#'>" +
        i18n("comment-reply") +
        "</a>" +
        "<a class='nikas-edit' href='#'>" +
        i18n("comment-edit") +
        "</a>" +
        "<a class='nikas-delete' href='#'>" +
        i18n("comment-delete") +
        "</a>" +
        "</div>" + // .nikas-comment-footer
        "<div class='nikas-follow-up'></div>" +
        "</div>" + // .text-wrapper
        "</div>"
    ); // .nikas-comment
};
module.exports = html;


/***/ }),

/***/ "./nikas/js/app/templates/postbox.js":
/*!*******************************************!*\
  !*** ./nikas/js/app/templates/postbox.js ***!
  \*******************************************/
/***/ (function(module) {

var html = function (globals) {
    var i18n = globals.i18n;
    var author = globals.author;
    var email = globals.email;
    var website = globals.website;

    return (
        "" +
        "<div class='nikas-postbox'>" +
        "<p class='nikas-copyright'>Powered by<a href='https://www.nikasproject.ir' target='_blank'>Nikas</a></p>" +
        "<div class='nikas-form-wrapper'>" +
        "<div class='nikas-textarea-wrapper'>" +
        "<div class='nikas-textarea nikas-placeholder' contenteditable='true'>" +
        i18n("postbox-text") +
        "</div>" +
        "<div class='nikas-preview'>" +
        "<div class='nikas-comment'>" +
        "<div class='nikas-text-wrapper'>" +
        "<div class='nikas-text'></div>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "<section class='nikas-auth-section'>" +
        "<p class='nikas-input-wrapper'>" +
        "<input type='text' name='author' placeholder='" +
        i18n("postbox-author") +
        "' value='" +
        (author ? author : "") +
        "' />" +
        "</p>" +
        "<p class='nikas-input-wrapper'>" +
        "<input type='email' name='email' placeholder='" +
        i18n("postbox-email") +
        "' value='" +
        (email ? email : "") +
        "' />" +
        "</p>" +
        "<p class='nikas-input-wrapper'>" +
        "<input type='text' name='website' placeholder='" +
        i18n("postbox-website") +
        "' value='" +
        (website ? website : "") +
        "' />" +
        "</p>" +
        "<p class='nikas-post-action'>" +
        "<input type='submit' value='" +
        i18n("postbox-submit") +
        "' />" +
        "</p>" +
        "<p class='nikas-post-action'>" +
        "<input type='button' name='preview' value='" +
        i18n("postbox-preview") +
        "' />" +
        "</p>" +
        "<p class='nikas-post-action'>" +
        "<input type='button' name='edit' value='" +
        i18n("postbox-edit") +
        "' />" +
        "</p>" +
        "</section>" +
        "<section class='nikas-notification-section'>" +
        "<label>" +
        "<input type='checkbox' name='notification' />" +
        i18n("postbox-notification") +
        "</label>" +
        "</section>" +
        "</div>" +
        "</div>"
    );
};
module.exports = html;


/***/ }),

/***/ "./nikas/js/app/utils.js":
/*!*******************************!*\
  !*** ./nikas/js/app/utils.js ***!
  \*******************************/
/***/ (function(module) {

"use strict";


// return `cookie` string if set
var cookie = function (cookie) {
    return (document.cookie.match("(^|; )" + cookie + "=([^;]*)") || 0)[2];
};

var pad = function (n, width, z) {
    z = z || "0";
    n = n + "";
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
};

var HTMLEntity = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
    "/": "&#x2F;",
};

var escape = function (html) {
    return String(html).replace(/[&<>"'\/]/g, function (s) {
        return HTMLEntity[s];
    });
};

var text = function (html) {
    var _ = document.createElement("div");
    _.innerHTML = html
        .replace(/<div><br><\/div>/gi, "<br>")
        .replace(/<div>/gi, "<br>")
        .replace(/<br>/gi, "\n")
        .replace(/&nbsp;/gi, " ");
    return _.textContent.trim();
};

var detext = function (text) {
    text = escape(text);
    return text
        .replace(/\n\n/gi, "<br><div><br></div>")
        .replace(/\n/gi, "<br>");
};

// Normalize a BCP47 language tag.
// Quoting https://tools.ietf.org/html/bcp47 :
//   An implementation can reproduce this format without accessing
//   the registry as follows.  All subtags, including extension
//   and private use subtags, use lowercase letters with two
//   exceptions: two-letter and four-letter subtags that neither
//   appear at the start of the tag nor occur after singletons.
//   Such two-letter subtags are all uppercase (as in the tags
//   "en-CA-x-ca" or "sgn-BE-FR") and four-letter subtags are
//   titlecase (as in the tag "az-Latn-x-latn").
// We also map underscores to dashes.
var normalize_bcp47 = function (tag) {
    var subtags = tag.toLowerCase().split(/[_-]/);
    var afterSingleton = false;
    for (var i = 0; i < subtags.length; i++) {
        if (subtags[i].length === 1) {
            afterSingleton = true;
        } else if (afterSingleton || i === 0) {
            afterSingleton = false;
        } else if (subtags[i].length === 2) {
            subtags[i] = subtags[i].toUpperCase();
        } else if (subtags[i].length === 4) {
            subtags[i] =
                subtags[i].charAt(0).toUpperCase() + subtags[i].substr(1);
        }
    }
    return subtags.join("-");
};

// Safari private browsing mode supports localStorage, but throws QUOTA_EXCEEDED_ERR
var localStorageImpl;
try {
    localStorage.setItem("x", "y");
    localStorage.removeItem("x");
    localStorageImpl = localStorage;
} catch (ex) {
    localStorageImpl = (function (storage) {
        return {
            setItem: function (key, val) {
                storage[key] = val;
            },
            getItem: function (key) {
                return typeof storage[key] !== "undefined"
                    ? storage[key]
                    : null;
            },
            removeItem: function (key) {
                delete storage[key];
            },
        };
    })({});
}

module.exports = {
    cookie: cookie,
    detext: detext,
    localStorageImpl: localStorageImpl,
    normalize_bcp47: normalize_bcp47,
    pad: pad,
    text: text,
};


/***/ }),

/***/ "./nikas/js/app/svg/arrow-down.svg":
/*!*****************************************!*\
  !*** ./nikas/js/app/svg/arrow-down.svg ***!
  \*****************************************/
/***/ (function(module) {

"use strict";
module.exports = "<svg width=\"16\"\n    height=\"16\"\n    viewBox=\"0 0 32 32\"\n    xmlns=\"http://www.w3.org/2000/svg\"\n    xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n    fill=\"gray\">\n    <g>\n        <path d=\"M 24.773,13.701c-0.651,0.669-7.512,7.205-7.512,7.205C 16.912,21.262, 16.456,21.44, 16,21.44c-0.458,0-0.914-0.178-1.261-0.534 c0,0-6.861-6.536-7.514-7.205c-0.651-0.669-0.696-1.87,0-2.586c 0.698-0.714, 1.669-0.77, 2.522,0L 16,17.112l 6.251-5.995 c 0.854-0.77, 1.827-0.714, 2.522,0C 25.47,11.83, 25.427,13.034, 24.773,13.701z\">\n        </path>\n    </g>\n</svg>\n";

/***/ }),

/***/ "./nikas/js/app/svg/arrow-up.svg":
/*!***************************************!*\
  !*** ./nikas/js/app/svg/arrow-up.svg ***!
  \***************************************/
/***/ (function(module) {

"use strict";
module.exports = "<svg width=\"16\"\n    height=\"16\"\n    viewBox=\"0 0 32 32\"\n    xmlns=\"http://www.w3.org/2000/svg\"\n    xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n    fill=\"gray\">\n    <g>\n        <path d=\"M 24.773,18.299c-0.651-0.669-7.512-7.203-7.512-7.203C 16.912,10.739, 16.456,10.56, 16,10.56c-0.458,0-0.914,0.179-1.261,0.536 c0,0-6.861,6.534-7.514,7.203c-0.651,0.669-0.696,1.872,0,2.586c 0.698,0.712, 1.669,0.77, 2.522,0L 16,14.89l 6.251,5.995 c 0.854,0.77, 1.827,0.712, 2.522,0C 25.47,20.17, 25.427,18.966, 24.773,18.299z\">\n        </path>\n    </g>\n</svg>\n";

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
!function() {
/*!***************************!*\
  !*** ./nikas/js/embed.js ***!
  \***************************/
var domready = __webpack_require__(/*! app/lib/ready */ "./nikas/js/app/lib/ready.js");
var config = __webpack_require__(/*! app/config */ "./nikas/js/app/config.js");
var i18n = __webpack_require__(/*! app/i18n */ "./nikas/js/app/i18n.js");
var api = __webpack_require__(/*! app/api */ "./nikas/js/app/api.js");
var nikas = __webpack_require__(/*! app/nikas */ "./nikas/js/app/nikas.js");
var count = __webpack_require__(/*! app/count */ "./nikas/js/app/count.js");
var $ = __webpack_require__(/*! app/dom */ "./nikas/js/app/dom.js");
var svg = __webpack_require__(/*! app/svg */ "./nikas/js/app/svg.js");
var template = __webpack_require__(/*! app/template */ "./nikas/js/app/template.js");

("use strict");

template.set("conf", config);
template.set("i18n", i18n.translate);
template.set("pluralize", i18n.pluralize);
template.set("svg", svg);

var nikas_thread;
var heading;

function init() {
    nikas_thread = $("#nikas-thread");
    heading = $.new("h4");

    if (config["css"] && $("style#nikas-style") === null) {
        var style = $.new("link");
        style.id = "nikas-style";
        style.rel = "stylesheet";
        style.type = "text/css";
        style.href = config["css-url"]
            ? config["css-url"]
            : api.endpoint + "/css/nikas.css";
        $("head").append(style);
    }

    count();

    if (nikas_thread === null) {
        return console.log("abort, #nikas-thread is missing");
    }

    if (config["feed"]) {
        var feedLink = $.new("a", i18n.translate("atom-feed"));
        var feedLinkWrapper = $.new("span.nikas-feedlink");
        feedLink.href = api.feed(nikas_thread.getAttribute("data-nikas-id"));
        feedLinkWrapper.appendChild(feedLink);
        nikas_thread.append(feedLinkWrapper);
    }
    // Note: Not appending the nikas.Postbox here since it relies
    // on the config object populated by elements fetched from the server,
    // and the call to fetch those is in fetchComments()
    nikas_thread.append(heading);
    nikas_thread.append('<div id="nikas-root"></div>');
}

function fetchComments() {
    if (!$("#nikas-root")) {
        return;
    }

    var nikas_root = $("#nikas-root");
    nikas_root.textContent = "";
    api.fetch(
        nikas_thread.getAttribute("data-nikas-id") || location.pathname,
        config["max-comments-top"],
        config["max-comments-nested"]
    ).then(
        function (rv) {
            for (var setting in rv.config) {
                if (
                    setting in config &&
                    config[setting] != rv.config[setting]
                ) {
                    console.log(
                        "Nikas: Client value '%s' for setting '%s' overridden by server value '%s'.\n" +
                            "Since Nikas version 0.12.6, 'data-nikas-%s' is only configured via the server " +
                            "to keep client and server in sync",
                        config[setting],
                        setting,
                        rv.config[setting],
                        setting
                    );
                }
                config[setting] = rv.config[setting];
            }

            // Note: nikas.Postbox relies on the config object populated by elements
            // fetched from the server, so it cannot be created in init()
            nikas_root.prepend(new nikas.Postbox(null));

            if (rv.total_replies === 0) {
                heading.textContent = i18n.translate("no-comments");
                return;
            }

            var lastcreated = 0;
            var count = rv.total_replies;
            rv.replies.forEach(function (comment) {
                nikas.insert(comment, false);
                if (comment.created > lastcreated) {
                    lastcreated = comment.created;
                }
                count = count + comment.total_replies;
            });
            heading.textContent = i18n.pluralize("num-comments", count);

            if (rv.hidden_replies > 0) {
                nikas.insert_loader(rv, lastcreated);
            }

            if (
                window.location.hash.length > 0 &&
                window.location.hash.match("^#nikas-[0-9]+$")
            ) {
                $(window.location.hash).scrollIntoView();
            }
        },
        function (err) {
            console.log(err);
        }
    );
}

domready(function () {
    init();
    fetchComments();
});

window.Nikas = {
    init: init,
    fetchComments: fetchComments,
};

}();
/******/ })()
;
//# sourceMappingURL=embed.dev.js.map