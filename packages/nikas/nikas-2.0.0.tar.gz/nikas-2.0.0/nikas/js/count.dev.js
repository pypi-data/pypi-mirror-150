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
  !*** ./nikas/js/count.js ***!
  \***************************/
var domready = __webpack_require__(/*! app/lib/ready */ "./nikas/js/app/lib/ready.js");
var count = __webpack_require__(/*! app/count */ "./nikas/js/app/count.js");

domready(function () {
    count();
});

}();
/******/ })()
;
//# sourceMappingURL=count.dev.js.map