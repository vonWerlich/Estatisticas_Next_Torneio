var Zi = { exports: {} }, Dr = {}, Ji = { exports: {} }, q = {};
var mc;
function up() {
  if (mc) return q;
  mc = 1;
  var l = /* @__PURE__ */ Symbol.for("react.element"), u = /* @__PURE__ */ Symbol.for("react.portal"), s = /* @__PURE__ */ Symbol.for("react.fragment"), c = /* @__PURE__ */ Symbol.for("react.strict_mode"), f = /* @__PURE__ */ Symbol.for("react.profiler"), m = /* @__PURE__ */ Symbol.for("react.provider"), k = /* @__PURE__ */ Symbol.for("react.context"), E = /* @__PURE__ */ Symbol.for("react.forward_ref"), z = /* @__PURE__ */ Symbol.for("react.suspense"), S = /* @__PURE__ */ Symbol.for("react.memo"), j = /* @__PURE__ */ Symbol.for("react.lazy"), M = Symbol.iterator;
  function B(v) {
    return v === null || typeof v != "object" ? null : (v = M && v[M] || v["@@iterator"], typeof v == "function" ? v : null);
  }
  var $ = { isMounted: function() {
    return !1;
  }, enqueueForceUpdate: function() {
  }, enqueueReplaceState: function() {
  }, enqueueSetState: function() {
  } }, Q = Object.assign, O = {};
  function Y(v, _, K) {
    this.props = v, this.context = _, this.refs = O, this.updater = K || $;
  }
  Y.prototype.isReactComponent = {}, Y.prototype.setState = function(v, _) {
    if (typeof v != "object" && typeof v != "function" && v != null) throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
    this.updater.enqueueSetState(this, v, _, "setState");
  }, Y.prototype.forceUpdate = function(v) {
    this.updater.enqueueForceUpdate(this, v, "forceUpdate");
  };
  function ve() {
  }
  ve.prototype = Y.prototype;
  function ue(v, _, K) {
    this.props = v, this.context = _, this.refs = O, this.updater = K || $;
  }
  var Le = ue.prototype = new ve();
  Le.constructor = ue, Q(Le, Y.prototype), Le.isPureReactComponent = !0;
  var we = Array.isArray, pe = Object.prototype.hasOwnProperty, Ce = { current: null }, Ee = { key: !0, ref: !0, __self: !0, __source: !0 };
  function G(v, _, K) {
    var X, J = {}, b = null, re = null;
    if (_ != null) for (X in _.ref !== void 0 && (re = _.ref), _.key !== void 0 && (b = "" + _.key), _) pe.call(_, X) && !Ee.hasOwnProperty(X) && (J[X] = _[X]);
    var ne = arguments.length - 2;
    if (ne === 1) J.children = K;
    else if (1 < ne) {
      for (var se = Array(ne), be = 0; be < ne; be++) se[be] = arguments[be + 2];
      J.children = se;
    }
    if (v && v.defaultProps) for (X in ne = v.defaultProps, ne) J[X] === void 0 && (J[X] = ne[X]);
    return { $$typeof: l, type: v, key: b, ref: re, props: J, _owner: Ce.current };
  }
  function Be(v, _) {
    return { $$typeof: l, type: v.type, key: _, ref: v.ref, props: v.props, _owner: v._owner };
  }
  function ke(v) {
    return typeof v == "object" && v !== null && v.$$typeof === l;
  }
  function Ne(v) {
    var _ = { "=": "=0", ":": "=2" };
    return "$" + v.replace(/[=:]/g, function(K) {
      return _[K];
    });
  }
  var Ae = /\/+/g;
  function Je(v, _) {
    return typeof v == "object" && v !== null && v.key != null ? Ne("" + v.key) : _.toString(36);
  }
  function pn(v, _, K, X, J) {
    var b = typeof v;
    (b === "undefined" || b === "boolean") && (v = null);
    var re = !1;
    if (v === null) re = !0;
    else switch (b) {
      case "string":
      case "number":
        re = !0;
        break;
      case "object":
        switch (v.$$typeof) {
          case l:
          case u:
            re = !0;
        }
    }
    if (re) return re = v, J = J(re), v = X === "" ? "." + Je(re, 0) : X, we(J) ? (K = "", v != null && (K = v.replace(Ae, "$&/") + "/"), pn(J, _, K, "", function(be) {
      return be;
    })) : J != null && (ke(J) && (J = Be(J, K + (!J.key || re && re.key === J.key ? "" : ("" + J.key).replace(Ae, "$&/") + "/") + v)), _.push(J)), 1;
    if (re = 0, X = X === "" ? "." : X + ":", we(v)) for (var ne = 0; ne < v.length; ne++) {
      b = v[ne];
      var se = X + Je(b, ne);
      re += pn(b, _, K, se, J);
    }
    else if (se = B(v), typeof se == "function") for (v = se.call(v), ne = 0; !(b = v.next()).done; ) b = b.value, se = X + Je(b, ne++), re += pn(b, _, K, se, J);
    else if (b === "object") throw _ = String(v), Error("Objects are not valid as a React child (found: " + (_ === "[object Object]" ? "object with keys {" + Object.keys(v).join(", ") + "}" : _) + "). If you meant to render a collection of children, use an array instead.");
    return re;
  }
  function Sn(v, _, K) {
    if (v == null) return v;
    var X = [], J = 0;
    return pn(v, X, "", "", function(b) {
      return _.call(K, b, J++);
    }), X;
  }
  function Ve(v) {
    if (v._status === -1) {
      var _ = v._result;
      _ = _(), _.then(function(K) {
        (v._status === 0 || v._status === -1) && (v._status = 1, v._result = K);
      }, function(K) {
        (v._status === 0 || v._status === -1) && (v._status = 2, v._result = K);
      }), v._status === -1 && (v._status = 0, v._result = _);
    }
    if (v._status === 1) return v._result.default;
    throw v._result;
  }
  var he = { current: null }, T = { transition: null }, H = { ReactCurrentDispatcher: he, ReactCurrentBatchConfig: T, ReactCurrentOwner: Ce };
  function D() {
    throw Error("act(...) is not supported in production builds of React.");
  }
  return q.Children = { map: Sn, forEach: function(v, _, K) {
    Sn(v, function() {
      _.apply(this, arguments);
    }, K);
  }, count: function(v) {
    var _ = 0;
    return Sn(v, function() {
      _++;
    }), _;
  }, toArray: function(v) {
    return Sn(v, function(_) {
      return _;
    }) || [];
  }, only: function(v) {
    if (!ke(v)) throw Error("React.Children.only expected to receive a single React element child.");
    return v;
  } }, q.Component = Y, q.Fragment = s, q.Profiler = f, q.PureComponent = ue, q.StrictMode = c, q.Suspense = z, q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = H, q.act = D, q.cloneElement = function(v, _, K) {
    if (v == null) throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + v + ".");
    var X = Q({}, v.props), J = v.key, b = v.ref, re = v._owner;
    if (_ != null) {
      if (_.ref !== void 0 && (b = _.ref, re = Ce.current), _.key !== void 0 && (J = "" + _.key), v.type && v.type.defaultProps) var ne = v.type.defaultProps;
      for (se in _) pe.call(_, se) && !Ee.hasOwnProperty(se) && (X[se] = _[se] === void 0 && ne !== void 0 ? ne[se] : _[se]);
    }
    var se = arguments.length - 2;
    if (se === 1) X.children = K;
    else if (1 < se) {
      ne = Array(se);
      for (var be = 0; be < se; be++) ne[be] = arguments[be + 2];
      X.children = ne;
    }
    return { $$typeof: l, type: v.type, key: J, ref: b, props: X, _owner: re };
  }, q.createContext = function(v) {
    return v = { $$typeof: k, _currentValue: v, _currentValue2: v, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null }, v.Provider = { $$typeof: m, _context: v }, v.Consumer = v;
  }, q.createElement = G, q.createFactory = function(v) {
    var _ = G.bind(null, v);
    return _.type = v, _;
  }, q.createRef = function() {
    return { current: null };
  }, q.forwardRef = function(v) {
    return { $$typeof: E, render: v };
  }, q.isValidElement = ke, q.lazy = function(v) {
    return { $$typeof: j, _payload: { _status: -1, _result: v }, _init: Ve };
  }, q.memo = function(v, _) {
    return { $$typeof: S, type: v, compare: _ === void 0 ? null : _ };
  }, q.startTransition = function(v) {
    var _ = T.transition;
    T.transition = {};
    try {
      v();
    } finally {
      T.transition = _;
    }
  }, q.unstable_act = D, q.useCallback = function(v, _) {
    return he.current.useCallback(v, _);
  }, q.useContext = function(v) {
    return he.current.useContext(v);
  }, q.useDebugValue = function() {
  }, q.useDeferredValue = function(v) {
    return he.current.useDeferredValue(v);
  }, q.useEffect = function(v, _) {
    return he.current.useEffect(v, _);
  }, q.useId = function() {
    return he.current.useId();
  }, q.useImperativeHandle = function(v, _, K) {
    return he.current.useImperativeHandle(v, _, K);
  }, q.useInsertionEffect = function(v, _) {
    return he.current.useInsertionEffect(v, _);
  }, q.useLayoutEffect = function(v, _) {
    return he.current.useLayoutEffect(v, _);
  }, q.useMemo = function(v, _) {
    return he.current.useMemo(v, _);
  }, q.useReducer = function(v, _, K) {
    return he.current.useReducer(v, _, K);
  }, q.useRef = function(v) {
    return he.current.useRef(v);
  }, q.useState = function(v) {
    return he.current.useState(v);
  }, q.useSyncExternalStore = function(v, _, K) {
    return he.current.useSyncExternalStore(v, _, K);
  }, q.useTransition = function() {
    return he.current.useTransition();
  }, q.version = "18.3.1", q;
}
var vc;
function fu() {
  return vc || (vc = 1, Ji.exports = up()), Ji.exports;
}
var gc;
function sp() {
  if (gc) return Dr;
  gc = 1;
  var l = fu(), u = /* @__PURE__ */ Symbol.for("react.element"), s = /* @__PURE__ */ Symbol.for("react.fragment"), c = Object.prototype.hasOwnProperty, f = l.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, m = { key: !0, ref: !0, __self: !0, __source: !0 };
  function k(E, z, S) {
    var j, M = {}, B = null, $ = null;
    S !== void 0 && (B = "" + S), z.key !== void 0 && (B = "" + z.key), z.ref !== void 0 && ($ = z.ref);
    for (j in z) c.call(z, j) && !m.hasOwnProperty(j) && (M[j] = z[j]);
    if (E && E.defaultProps) for (j in z = E.defaultProps, z) M[j] === void 0 && (M[j] = z[j]);
    return { $$typeof: u, type: E, key: B, ref: $, props: M, _owner: f.current };
  }
  return Dr.Fragment = s, Dr.jsx = k, Dr.jsxs = k, Dr;
}
var yc;
function ap() {
  return yc || (yc = 1, Zi.exports = sp()), Zi.exports;
}
var iu = ap(), Gl = fu(), ql = {}, bi = { exports: {} }, Xe = {}, eu = { exports: {} }, nu = {};
var wc;
function cp() {
  return wc || (wc = 1, (function(l) {
    function u(T, H) {
      var D = T.length;
      T.push(H);
      e: for (; 0 < D; ) {
        var v = D - 1 >>> 1, _ = T[v];
        if (0 < f(_, H)) T[v] = H, T[D] = _, D = v;
        else break e;
      }
    }
    function s(T) {
      return T.length === 0 ? null : T[0];
    }
    function c(T) {
      if (T.length === 0) return null;
      var H = T[0], D = T.pop();
      if (D !== H) {
        T[0] = D;
        e: for (var v = 0, _ = T.length, K = _ >>> 1; v < K; ) {
          var X = 2 * (v + 1) - 1, J = T[X], b = X + 1, re = T[b];
          if (0 > f(J, D)) b < _ && 0 > f(re, J) ? (T[v] = re, T[b] = D, v = b) : (T[v] = J, T[X] = D, v = X);
          else if (b < _ && 0 > f(re, D)) T[v] = re, T[b] = D, v = b;
          else break e;
        }
      }
      return H;
    }
    function f(T, H) {
      var D = T.sortIndex - H.sortIndex;
      return D !== 0 ? D : T.id - H.id;
    }
    if (typeof performance == "object" && typeof performance.now == "function") {
      var m = performance;
      l.unstable_now = function() {
        return m.now();
      };
    } else {
      var k = Date, E = k.now();
      l.unstable_now = function() {
        return k.now() - E;
      };
    }
    var z = [], S = [], j = 1, M = null, B = 3, $ = !1, Q = !1, O = !1, Y = typeof setTimeout == "function" ? setTimeout : null, ve = typeof clearTimeout == "function" ? clearTimeout : null, ue = typeof setImmediate < "u" ? setImmediate : null;
    typeof navigator < "u" && navigator.scheduling !== void 0 && navigator.scheduling.isInputPending !== void 0 && navigator.scheduling.isInputPending.bind(navigator.scheduling);
    function Le(T) {
      for (var H = s(S); H !== null; ) {
        if (H.callback === null) c(S);
        else if (H.startTime <= T) c(S), H.sortIndex = H.expirationTime, u(z, H);
        else break;
        H = s(S);
      }
    }
    function we(T) {
      if (O = !1, Le(T), !Q) if (s(z) !== null) Q = !0, Ve(pe);
      else {
        var H = s(S);
        H !== null && he(we, H.startTime - T);
      }
    }
    function pe(T, H) {
      Q = !1, O && (O = !1, ve(G), G = -1), $ = !0;
      var D = B;
      try {
        for (Le(H), M = s(z); M !== null && (!(M.expirationTime > H) || T && !Ne()); ) {
          var v = M.callback;
          if (typeof v == "function") {
            M.callback = null, B = M.priorityLevel;
            var _ = v(M.expirationTime <= H);
            H = l.unstable_now(), typeof _ == "function" ? M.callback = _ : M === s(z) && c(z), Le(H);
          } else c(z);
          M = s(z);
        }
        if (M !== null) var K = !0;
        else {
          var X = s(S);
          X !== null && he(we, X.startTime - H), K = !1;
        }
        return K;
      } finally {
        M = null, B = D, $ = !1;
      }
    }
    var Ce = !1, Ee = null, G = -1, Be = 5, ke = -1;
    function Ne() {
      return !(l.unstable_now() - ke < Be);
    }
    function Ae() {
      if (Ee !== null) {
        var T = l.unstable_now();
        ke = T;
        var H = !0;
        try {
          H = Ee(!0, T);
        } finally {
          H ? Je() : (Ce = !1, Ee = null);
        }
      } else Ce = !1;
    }
    var Je;
    if (typeof ue == "function") Je = function() {
      ue(Ae);
    };
    else if (typeof MessageChannel < "u") {
      var pn = new MessageChannel(), Sn = pn.port2;
      pn.port1.onmessage = Ae, Je = function() {
        Sn.postMessage(null);
      };
    } else Je = function() {
      Y(Ae, 0);
    };
    function Ve(T) {
      Ee = T, Ce || (Ce = !0, Je());
    }
    function he(T, H) {
      G = Y(function() {
        T(l.unstable_now());
      }, H);
    }
    l.unstable_IdlePriority = 5, l.unstable_ImmediatePriority = 1, l.unstable_LowPriority = 4, l.unstable_NormalPriority = 3, l.unstable_Profiling = null, l.unstable_UserBlockingPriority = 2, l.unstable_cancelCallback = function(T) {
      T.callback = null;
    }, l.unstable_continueExecution = function() {
      Q || $ || (Q = !0, Ve(pe));
    }, l.unstable_forceFrameRate = function(T) {
      0 > T || 125 < T ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : Be = 0 < T ? Math.floor(1e3 / T) : 5;
    }, l.unstable_getCurrentPriorityLevel = function() {
      return B;
    }, l.unstable_getFirstCallbackNode = function() {
      return s(z);
    }, l.unstable_next = function(T) {
      switch (B) {
        case 1:
        case 2:
        case 3:
          var H = 3;
          break;
        default:
          H = B;
      }
      var D = B;
      B = H;
      try {
        return T();
      } finally {
        B = D;
      }
    }, l.unstable_pauseExecution = function() {
    }, l.unstable_requestPaint = function() {
    }, l.unstable_runWithPriority = function(T, H) {
      switch (T) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
          break;
        default:
          T = 3;
      }
      var D = B;
      B = T;
      try {
        return H();
      } finally {
        B = D;
      }
    }, l.unstable_scheduleCallback = function(T, H, D) {
      var v = l.unstable_now();
      switch (typeof D == "object" && D !== null ? (D = D.delay, D = typeof D == "number" && 0 < D ? v + D : v) : D = v, T) {
        case 1:
          var _ = -1;
          break;
        case 2:
          _ = 250;
          break;
        case 5:
          _ = 1073741823;
          break;
        case 4:
          _ = 1e4;
          break;
        default:
          _ = 5e3;
      }
      return _ = D + _, T = { id: j++, callback: H, priorityLevel: T, startTime: D, expirationTime: _, sortIndex: -1 }, D > v ? (T.sortIndex = D, u(S, T), s(z) === null && T === s(S) && (O ? (ve(G), G = -1) : O = !0, he(we, D - v))) : (T.sortIndex = _, u(z, T), Q || $ || (Q = !0, Ve(pe))), T;
    }, l.unstable_shouldYield = Ne, l.unstable_wrapCallback = function(T) {
      var H = B;
      return function() {
        var D = B;
        B = H;
        try {
          return T.apply(this, arguments);
        } finally {
          B = D;
        }
      };
    };
  })(nu)), nu;
}
var kc;
function fp() {
  return kc || (kc = 1, eu.exports = cp()), eu.exports;
}
var Sc;
function dp() {
  if (Sc) return Xe;
  Sc = 1;
  var l = fu(), u = fp();
  function s(e) {
    for (var n = "https://reactjs.org/docs/error-decoder.html?invariant=" + e, t = 1; t < arguments.length; t++) n += "&args[]=" + encodeURIComponent(arguments[t]);
    return "Minified React error #" + e + "; visit " + n + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  var c = /* @__PURE__ */ new Set(), f = {};
  function m(e, n) {
    k(e, n), k(e + "Capture", n);
  }
  function k(e, n) {
    for (f[e] = n, e = 0; e < n.length; e++) c.add(n[e]);
  }
  var E = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), z = Object.prototype.hasOwnProperty, S = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, j = {}, M = {};
  function B(e) {
    return z.call(M, e) ? !0 : z.call(j, e) ? !1 : S.test(e) ? M[e] = !0 : (j[e] = !0, !1);
  }
  function $(e, n, t, r) {
    if (t !== null && t.type === 0) return !1;
    switch (typeof n) {
      case "function":
      case "symbol":
        return !0;
      case "boolean":
        return r ? !1 : t !== null ? !t.acceptsBooleans : (e = e.toLowerCase().slice(0, 5), e !== "data-" && e !== "aria-");
      default:
        return !1;
    }
  }
  function Q(e, n, t, r) {
    if (n === null || typeof n > "u" || $(e, n, t, r)) return !0;
    if (r) return !1;
    if (t !== null) switch (t.type) {
      case 3:
        return !n;
      case 4:
        return n === !1;
      case 5:
        return isNaN(n);
      case 6:
        return isNaN(n) || 1 > n;
    }
    return !1;
  }
  function O(e, n, t, r, o, i, a) {
    this.acceptsBooleans = n === 2 || n === 3 || n === 4, this.attributeName = r, this.attributeNamespace = o, this.mustUseProperty = t, this.propertyName = e, this.type = n, this.sanitizeURL = i, this.removeEmptyString = a;
  }
  var Y = {};
  "children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(e) {
    Y[e] = new O(e, 0, !1, e, null, !1, !1);
  }), [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(e) {
    var n = e[0];
    Y[n] = new O(n, 1, !1, e[1], null, !1, !1);
  }), ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(e) {
    Y[e] = new O(e, 2, !1, e.toLowerCase(), null, !1, !1);
  }), ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(e) {
    Y[e] = new O(e, 2, !1, e, null, !1, !1);
  }), "allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(e) {
    Y[e] = new O(e, 3, !1, e.toLowerCase(), null, !1, !1);
  }), ["checked", "multiple", "muted", "selected"].forEach(function(e) {
    Y[e] = new O(e, 3, !0, e, null, !1, !1);
  }), ["capture", "download"].forEach(function(e) {
    Y[e] = new O(e, 4, !1, e, null, !1, !1);
  }), ["cols", "rows", "size", "span"].forEach(function(e) {
    Y[e] = new O(e, 6, !1, e, null, !1, !1);
  }), ["rowSpan", "start"].forEach(function(e) {
    Y[e] = new O(e, 5, !1, e.toLowerCase(), null, !1, !1);
  });
  var ve = /[\-:]([a-z])/g;
  function ue(e) {
    return e[1].toUpperCase();
  }
  "accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(e) {
    var n = e.replace(
      ve,
      ue
    );
    Y[n] = new O(n, 1, !1, e, null, !1, !1);
  }), "xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(e) {
    var n = e.replace(ve, ue);
    Y[n] = new O(n, 1, !1, e, "http://www.w3.org/1999/xlink", !1, !1);
  }), ["xml:base", "xml:lang", "xml:space"].forEach(function(e) {
    var n = e.replace(ve, ue);
    Y[n] = new O(n, 1, !1, e, "http://www.w3.org/XML/1998/namespace", !1, !1);
  }), ["tabIndex", "crossOrigin"].forEach(function(e) {
    Y[e] = new O(e, 1, !1, e.toLowerCase(), null, !1, !1);
  }), Y.xlinkHref = new O("xlinkHref", 1, !1, "xlink:href", "http://www.w3.org/1999/xlink", !0, !1), ["src", "href", "action", "formAction"].forEach(function(e) {
    Y[e] = new O(e, 1, !1, e.toLowerCase(), null, !0, !0);
  });
  function Le(e, n, t, r) {
    var o = Y.hasOwnProperty(n) ? Y[n] : null;
    (o !== null ? o.type !== 0 : r || !(2 < n.length) || n[0] !== "o" && n[0] !== "O" || n[1] !== "n" && n[1] !== "N") && (Q(n, t, o, r) && (t = null), r || o === null ? B(n) && (t === null ? e.removeAttribute(n) : e.setAttribute(n, "" + t)) : o.mustUseProperty ? e[o.propertyName] = t === null ? o.type === 3 ? !1 : "" : t : (n = o.attributeName, r = o.attributeNamespace, t === null ? e.removeAttribute(n) : (o = o.type, t = o === 3 || o === 4 && t === !0 ? "" : "" + t, r ? e.setAttributeNS(r, n, t) : e.setAttribute(n, t))));
  }
  var we = l.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, pe = /* @__PURE__ */ Symbol.for("react.element"), Ce = /* @__PURE__ */ Symbol.for("react.portal"), Ee = /* @__PURE__ */ Symbol.for("react.fragment"), G = /* @__PURE__ */ Symbol.for("react.strict_mode"), Be = /* @__PURE__ */ Symbol.for("react.profiler"), ke = /* @__PURE__ */ Symbol.for("react.provider"), Ne = /* @__PURE__ */ Symbol.for("react.context"), Ae = /* @__PURE__ */ Symbol.for("react.forward_ref"), Je = /* @__PURE__ */ Symbol.for("react.suspense"), pn = /* @__PURE__ */ Symbol.for("react.suspense_list"), Sn = /* @__PURE__ */ Symbol.for("react.memo"), Ve = /* @__PURE__ */ Symbol.for("react.lazy"), he = /* @__PURE__ */ Symbol.for("react.offscreen"), T = Symbol.iterator;
  function H(e) {
    return e === null || typeof e != "object" ? null : (e = T && e[T] || e["@@iterator"], typeof e == "function" ? e : null);
  }
  var D = Object.assign, v;
  function _(e) {
    if (v === void 0) try {
      throw Error();
    } catch (t) {
      var n = t.stack.trim().match(/\n( *(at )?)/);
      v = n && n[1] || "";
    }
    return `
` + v + e;
  }
  var K = !1;
  function X(e, n) {
    if (!e || K) return "";
    K = !0;
    var t = Error.prepareStackTrace;
    Error.prepareStackTrace = void 0;
    try {
      if (n) if (n = function() {
        throw Error();
      }, Object.defineProperty(n.prototype, "props", { set: function() {
        throw Error();
      } }), typeof Reflect == "object" && Reflect.construct) {
        try {
          Reflect.construct(n, []);
        } catch (w) {
          var r = w;
        }
        Reflect.construct(e, [], n);
      } else {
        try {
          n.call();
        } catch (w) {
          r = w;
        }
        e.call(n.prototype);
      }
      else {
        try {
          throw Error();
        } catch (w) {
          r = w;
        }
        e();
      }
    } catch (w) {
      if (w && r && typeof w.stack == "string") {
        for (var o = w.stack.split(`
`), i = r.stack.split(`
`), a = o.length - 1, d = i.length - 1; 1 <= a && 0 <= d && o[a] !== i[d]; ) d--;
        for (; 1 <= a && 0 <= d; a--, d--) if (o[a] !== i[d]) {
          if (a !== 1 || d !== 1)
            do
              if (a--, d--, 0 > d || o[a] !== i[d]) {
                var p = `
` + o[a].replace(" at new ", " at ");
                return e.displayName && p.includes("<anonymous>") && (p = p.replace("<anonymous>", e.displayName)), p;
              }
            while (1 <= a && 0 <= d);
          break;
        }
      }
    } finally {
      K = !1, Error.prepareStackTrace = t;
    }
    return (e = e ? e.displayName || e.name : "") ? _(e) : "";
  }
  function J(e) {
    switch (e.tag) {
      case 5:
        return _(e.type);
      case 16:
        return _("Lazy");
      case 13:
        return _("Suspense");
      case 19:
        return _("SuspenseList");
      case 0:
      case 2:
      case 15:
        return e = X(e.type, !1), e;
      case 11:
        return e = X(e.type.render, !1), e;
      case 1:
        return e = X(e.type, !0), e;
      default:
        return "";
    }
  }
  function b(e) {
    if (e == null) return null;
    if (typeof e == "function") return e.displayName || e.name || null;
    if (typeof e == "string") return e;
    switch (e) {
      case Ee:
        return "Fragment";
      case Ce:
        return "Portal";
      case Be:
        return "Profiler";
      case G:
        return "StrictMode";
      case Je:
        return "Suspense";
      case pn:
        return "SuspenseList";
    }
    if (typeof e == "object") switch (e.$$typeof) {
      case Ne:
        return (e.displayName || "Context") + ".Consumer";
      case ke:
        return (e._context.displayName || "Context") + ".Provider";
      case Ae:
        var n = e.render;
        return e = e.displayName, e || (e = n.displayName || n.name || "", e = e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef"), e;
      case Sn:
        return n = e.displayName || null, n !== null ? n : b(e.type) || "Memo";
      case Ve:
        n = e._payload, e = e._init;
        try {
          return b(e(n));
        } catch {
        }
    }
    return null;
  }
  function re(e) {
    var n = e.type;
    switch (e.tag) {
      case 24:
        return "Cache";
      case 9:
        return (n.displayName || "Context") + ".Consumer";
      case 10:
        return (n._context.displayName || "Context") + ".Provider";
      case 18:
        return "DehydratedFragment";
      case 11:
        return e = n.render, e = e.displayName || e.name || "", n.displayName || (e !== "" ? "ForwardRef(" + e + ")" : "ForwardRef");
      case 7:
        return "Fragment";
      case 5:
        return n;
      case 4:
        return "Portal";
      case 3:
        return "Root";
      case 6:
        return "Text";
      case 16:
        return b(n);
      case 8:
        return n === G ? "StrictMode" : "Mode";
      case 22:
        return "Offscreen";
      case 12:
        return "Profiler";
      case 21:
        return "Scope";
      case 13:
        return "Suspense";
      case 19:
        return "SuspenseList";
      case 25:
        return "TracingMarker";
      case 1:
      case 0:
      case 17:
      case 2:
      case 14:
      case 15:
        if (typeof n == "function") return n.displayName || n.name || null;
        if (typeof n == "string") return n;
    }
    return null;
  }
  function ne(e) {
    switch (typeof e) {
      case "boolean":
      case "number":
      case "string":
      case "undefined":
        return e;
      case "object":
        return e;
      default:
        return "";
    }
  }
  function se(e) {
    var n = e.type;
    return (e = e.nodeName) && e.toLowerCase() === "input" && (n === "checkbox" || n === "radio");
  }
  function be(e) {
    var n = se(e) ? "checked" : "value", t = Object.getOwnPropertyDescriptor(e.constructor.prototype, n), r = "" + e[n];
    if (!e.hasOwnProperty(n) && typeof t < "u" && typeof t.get == "function" && typeof t.set == "function") {
      var o = t.get, i = t.set;
      return Object.defineProperty(e, n, { configurable: !0, get: function() {
        return o.call(this);
      }, set: function(a) {
        r = "" + a, i.call(this, a);
      } }), Object.defineProperty(e, n, { enumerable: t.enumerable }), { getValue: function() {
        return r;
      }, setValue: function(a) {
        r = "" + a;
      }, stopTracking: function() {
        e._valueTracker = null, delete e[n];
      } };
    }
  }
  function Ar(e) {
    e._valueTracker || (e._valueTracker = be(e));
  }
  function Su(e) {
    if (!e) return !1;
    var n = e._valueTracker;
    if (!n) return !0;
    var t = n.getValue(), r = "";
    return e && (r = se(e) ? e.checked ? "true" : "false" : e.value), e = r, e !== t ? (n.setValue(e), !0) : !1;
  }
  function Ur(e) {
    if (e = e || (typeof document < "u" ? document : void 0), typeof e > "u") return null;
    try {
      return e.activeElement || e.body;
    } catch {
      return e.body;
    }
  }
  function ro(e, n) {
    var t = n.checked;
    return D({}, n, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: t ?? e._wrapperState.initialChecked });
  }
  function Cu(e, n) {
    var t = n.defaultValue == null ? "" : n.defaultValue, r = n.checked != null ? n.checked : n.defaultChecked;
    t = ne(n.value != null ? n.value : t), e._wrapperState = { initialChecked: r, initialValue: t, controlled: n.type === "checkbox" || n.type === "radio" ? n.checked != null : n.value != null };
  }
  function Eu(e, n) {
    n = n.checked, n != null && Le(e, "checked", n, !1);
  }
  function lo(e, n) {
    Eu(e, n);
    var t = ne(n.value), r = n.type;
    if (t != null) r === "number" ? (t === 0 && e.value === "" || e.value != t) && (e.value = "" + t) : e.value !== "" + t && (e.value = "" + t);
    else if (r === "submit" || r === "reset") {
      e.removeAttribute("value");
      return;
    }
    n.hasOwnProperty("value") ? oo(e, n.type, t) : n.hasOwnProperty("defaultValue") && oo(e, n.type, ne(n.defaultValue)), n.checked == null && n.defaultChecked != null && (e.defaultChecked = !!n.defaultChecked);
  }
  function _u(e, n, t) {
    if (n.hasOwnProperty("value") || n.hasOwnProperty("defaultValue")) {
      var r = n.type;
      if (!(r !== "submit" && r !== "reset" || n.value !== void 0 && n.value !== null)) return;
      n = "" + e._wrapperState.initialValue, t || n === e.value || (e.value = n), e.defaultValue = n;
    }
    t = e.name, t !== "" && (e.name = ""), e.defaultChecked = !!e._wrapperState.initialChecked, t !== "" && (e.name = t);
  }
  function oo(e, n, t) {
    (n !== "number" || Ur(e.ownerDocument) !== e) && (t == null ? e.defaultValue = "" + e._wrapperState.initialValue : e.defaultValue !== "" + t && (e.defaultValue = "" + t));
  }
  var qt = Array.isArray;
  function Et(e, n, t, r) {
    if (e = e.options, n) {
      n = {};
      for (var o = 0; o < t.length; o++) n["$" + t[o]] = !0;
      for (t = 0; t < e.length; t++) o = n.hasOwnProperty("$" + e[t].value), e[t].selected !== o && (e[t].selected = o), o && r && (e[t].defaultSelected = !0);
    } else {
      for (t = "" + ne(t), n = null, o = 0; o < e.length; o++) {
        if (e[o].value === t) {
          e[o].selected = !0, r && (e[o].defaultSelected = !0);
          return;
        }
        n !== null || e[o].disabled || (n = e[o]);
      }
      n !== null && (n.selected = !0);
    }
  }
  function io(e, n) {
    if (n.dangerouslySetInnerHTML != null) throw Error(s(91));
    return D({}, n, { value: void 0, defaultValue: void 0, children: "" + e._wrapperState.initialValue });
  }
  function xu(e, n) {
    var t = n.value;
    if (t == null) {
      if (t = n.children, n = n.defaultValue, t != null) {
        if (n != null) throw Error(s(92));
        if (qt(t)) {
          if (1 < t.length) throw Error(s(93));
          t = t[0];
        }
        n = t;
      }
      n == null && (n = ""), t = n;
    }
    e._wrapperState = { initialValue: ne(t) };
  }
  function Pu(e, n) {
    var t = ne(n.value), r = ne(n.defaultValue);
    t != null && (t = "" + t, t !== e.value && (e.value = t), n.defaultValue == null && e.defaultValue !== t && (e.defaultValue = t)), r != null && (e.defaultValue = "" + r);
  }
  function Nu(e) {
    var n = e.textContent;
    n === e._wrapperState.initialValue && n !== "" && n !== null && (e.value = n);
  }
  function zu(e) {
    switch (e) {
      case "svg":
        return "http://www.w3.org/2000/svg";
      case "math":
        return "http://www.w3.org/1998/Math/MathML";
      default:
        return "http://www.w3.org/1999/xhtml";
    }
  }
  function uo(e, n) {
    return e == null || e === "http://www.w3.org/1999/xhtml" ? zu(n) : e === "http://www.w3.org/2000/svg" && n === "foreignObject" ? "http://www.w3.org/1999/xhtml" : e;
  }
  var Wr, Mu = (function(e) {
    return typeof MSApp < "u" && MSApp.execUnsafeLocalFunction ? function(n, t, r, o) {
      MSApp.execUnsafeLocalFunction(function() {
        return e(n, t, r, o);
      });
    } : e;
  })(function(e, n) {
    if (e.namespaceURI !== "http://www.w3.org/2000/svg" || "innerHTML" in e) e.innerHTML = n;
    else {
      for (Wr = Wr || document.createElement("div"), Wr.innerHTML = "<svg>" + n.valueOf().toString() + "</svg>", n = Wr.firstChild; e.firstChild; ) e.removeChild(e.firstChild);
      for (; n.firstChild; ) e.appendChild(n.firstChild);
    }
  });
  function Xt(e, n) {
    if (n) {
      var t = e.firstChild;
      if (t && t === e.lastChild && t.nodeType === 3) {
        t.nodeValue = n;
        return;
      }
    }
    e.textContent = n;
  }
  var Gt = {
    animationIterationCount: !0,
    aspectRatio: !0,
    borderImageOutset: !0,
    borderImageSlice: !0,
    borderImageWidth: !0,
    boxFlex: !0,
    boxFlexGroup: !0,
    boxOrdinalGroup: !0,
    columnCount: !0,
    columns: !0,
    flex: !0,
    flexGrow: !0,
    flexPositive: !0,
    flexShrink: !0,
    flexNegative: !0,
    flexOrder: !0,
    gridArea: !0,
    gridRow: !0,
    gridRowEnd: !0,
    gridRowSpan: !0,
    gridRowStart: !0,
    gridColumn: !0,
    gridColumnEnd: !0,
    gridColumnSpan: !0,
    gridColumnStart: !0,
    fontWeight: !0,
    lineClamp: !0,
    lineHeight: !0,
    opacity: !0,
    order: !0,
    orphans: !0,
    tabSize: !0,
    widows: !0,
    zIndex: !0,
    zoom: !0,
    fillOpacity: !0,
    floodOpacity: !0,
    stopOpacity: !0,
    strokeDasharray: !0,
    strokeDashoffset: !0,
    strokeMiterlimit: !0,
    strokeOpacity: !0,
    strokeWidth: !0
  }, ff = ["Webkit", "ms", "Moz", "O"];
  Object.keys(Gt).forEach(function(e) {
    ff.forEach(function(n) {
      n = n + e.charAt(0).toUpperCase() + e.substring(1), Gt[n] = Gt[e];
    });
  });
  function Tu(e, n, t) {
    return n == null || typeof n == "boolean" || n === "" ? "" : t || typeof n != "number" || n === 0 || Gt.hasOwnProperty(e) && Gt[e] ? ("" + n).trim() : n + "px";
  }
  function Lu(e, n) {
    e = e.style;
    for (var t in n) if (n.hasOwnProperty(t)) {
      var r = t.indexOf("--") === 0, o = Tu(t, n[t], r);
      t === "float" && (t = "cssFloat"), r ? e.setProperty(t, o) : e[t] = o;
    }
  }
  var df = D({ menuitem: !0 }, { area: !0, base: !0, br: !0, col: !0, embed: !0, hr: !0, img: !0, input: !0, keygen: !0, link: !0, meta: !0, param: !0, source: !0, track: !0, wbr: !0 });
  function so(e, n) {
    if (n) {
      if (df[e] && (n.children != null || n.dangerouslySetInnerHTML != null)) throw Error(s(137, e));
      if (n.dangerouslySetInnerHTML != null) {
        if (n.children != null) throw Error(s(60));
        if (typeof n.dangerouslySetInnerHTML != "object" || !("__html" in n.dangerouslySetInnerHTML)) throw Error(s(61));
      }
      if (n.style != null && typeof n.style != "object") throw Error(s(62));
    }
  }
  function ao(e, n) {
    if (e.indexOf("-") === -1) return typeof n.is == "string";
    switch (e) {
      case "annotation-xml":
      case "color-profile":
      case "font-face":
      case "font-face-src":
      case "font-face-uri":
      case "font-face-format":
      case "font-face-name":
      case "missing-glyph":
        return !1;
      default:
        return !0;
    }
  }
  var co = null;
  function fo(e) {
    return e = e.target || e.srcElement || window, e.correspondingUseElement && (e = e.correspondingUseElement), e.nodeType === 3 ? e.parentNode : e;
  }
  var po = null, _t = null, xt = null;
  function Ru(e) {
    if (e = yr(e)) {
      if (typeof po != "function") throw Error(s(280));
      var n = e.stateNode;
      n && (n = al(n), po(e.stateNode, e.type, n));
    }
  }
  function Du(e) {
    _t ? xt ? xt.push(e) : xt = [e] : _t = e;
  }
  function Ou() {
    if (_t) {
      var e = _t, n = xt;
      if (xt = _t = null, Ru(e), n) for (e = 0; e < n.length; e++) Ru(n[e]);
    }
  }
  function Iu(e, n) {
    return e(n);
  }
  function Fu() {
  }
  var ho = !1;
  function ju(e, n, t) {
    if (ho) return e(n, t);
    ho = !0;
    try {
      return Iu(e, n, t);
    } finally {
      ho = !1, (_t !== null || xt !== null) && (Fu(), Ou());
    }
  }
  function Zt(e, n) {
    var t = e.stateNode;
    if (t === null) return null;
    var r = al(t);
    if (r === null) return null;
    t = r[n];
    e: switch (n) {
      case "onClick":
      case "onClickCapture":
      case "onDoubleClick":
      case "onDoubleClickCapture":
      case "onMouseDown":
      case "onMouseDownCapture":
      case "onMouseMove":
      case "onMouseMoveCapture":
      case "onMouseUp":
      case "onMouseUpCapture":
      case "onMouseEnter":
        (r = !r.disabled) || (e = e.type, r = !(e === "button" || e === "input" || e === "select" || e === "textarea")), e = !r;
        break e;
      default:
        e = !1;
    }
    if (e) return null;
    if (t && typeof t != "function") throw Error(s(231, n, typeof t));
    return t;
  }
  var mo = !1;
  if (E) try {
    var Jt = {};
    Object.defineProperty(Jt, "passive", { get: function() {
      mo = !0;
    } }), window.addEventListener("test", Jt, Jt), window.removeEventListener("test", Jt, Jt);
  } catch {
    mo = !1;
  }
  function pf(e, n, t, r, o, i, a, d, p) {
    var w = Array.prototype.slice.call(arguments, 3);
    try {
      n.apply(t, w);
    } catch (x) {
      this.onError(x);
    }
  }
  var bt = !1, Hr = null, Br = !1, vo = null, hf = { onError: function(e) {
    bt = !0, Hr = e;
  } };
  function mf(e, n, t, r, o, i, a, d, p) {
    bt = !1, Hr = null, pf.apply(hf, arguments);
  }
  function vf(e, n, t, r, o, i, a, d, p) {
    if (mf.apply(this, arguments), bt) {
      if (bt) {
        var w = Hr;
        bt = !1, Hr = null;
      } else throw Error(s(198));
      Br || (Br = !0, vo = w);
    }
  }
  function it(e) {
    var n = e, t = e;
    if (e.alternate) for (; n.return; ) n = n.return;
    else {
      e = n;
      do
        n = e, (n.flags & 4098) !== 0 && (t = n.return), e = n.return;
      while (e);
    }
    return n.tag === 3 ? t : null;
  }
  function Au(e) {
    if (e.tag === 13) {
      var n = e.memoizedState;
      if (n === null && (e = e.alternate, e !== null && (n = e.memoizedState)), n !== null) return n.dehydrated;
    }
    return null;
  }
  function Uu(e) {
    if (it(e) !== e) throw Error(s(188));
  }
  function gf(e) {
    var n = e.alternate;
    if (!n) {
      if (n = it(e), n === null) throw Error(s(188));
      return n !== e ? null : e;
    }
    for (var t = e, r = n; ; ) {
      var o = t.return;
      if (o === null) break;
      var i = o.alternate;
      if (i === null) {
        if (r = o.return, r !== null) {
          t = r;
          continue;
        }
        break;
      }
      if (o.child === i.child) {
        for (i = o.child; i; ) {
          if (i === t) return Uu(o), e;
          if (i === r) return Uu(o), n;
          i = i.sibling;
        }
        throw Error(s(188));
      }
      if (t.return !== r.return) t = o, r = i;
      else {
        for (var a = !1, d = o.child; d; ) {
          if (d === t) {
            a = !0, t = o, r = i;
            break;
          }
          if (d === r) {
            a = !0, r = o, t = i;
            break;
          }
          d = d.sibling;
        }
        if (!a) {
          for (d = i.child; d; ) {
            if (d === t) {
              a = !0, t = i, r = o;
              break;
            }
            if (d === r) {
              a = !0, r = i, t = o;
              break;
            }
            d = d.sibling;
          }
          if (!a) throw Error(s(189));
        }
      }
      if (t.alternate !== r) throw Error(s(190));
    }
    if (t.tag !== 3) throw Error(s(188));
    return t.stateNode.current === t ? e : n;
  }
  function Wu(e) {
    return e = gf(e), e !== null ? Hu(e) : null;
  }
  function Hu(e) {
    if (e.tag === 5 || e.tag === 6) return e;
    for (e = e.child; e !== null; ) {
      var n = Hu(e);
      if (n !== null) return n;
      e = e.sibling;
    }
    return null;
  }
  var Bu = u.unstable_scheduleCallback, Vu = u.unstable_cancelCallback, yf = u.unstable_shouldYield, wf = u.unstable_requestPaint, ge = u.unstable_now, kf = u.unstable_getCurrentPriorityLevel, go = u.unstable_ImmediatePriority, $u = u.unstable_UserBlockingPriority, Vr = u.unstable_NormalPriority, Sf = u.unstable_LowPriority, Qu = u.unstable_IdlePriority, $r = null, Cn = null;
  function Cf(e) {
    if (Cn && typeof Cn.onCommitFiberRoot == "function") try {
      Cn.onCommitFiberRoot($r, e, void 0, (e.current.flags & 128) === 128);
    } catch {
    }
  }
  var hn = Math.clz32 ? Math.clz32 : xf, Ef = Math.log, _f = Math.LN2;
  function xf(e) {
    return e >>>= 0, e === 0 ? 32 : 31 - (Ef(e) / _f | 0) | 0;
  }
  var Qr = 64, Kr = 4194304;
  function er(e) {
    switch (e & -e) {
      case 1:
        return 1;
      case 2:
        return 2;
      case 4:
        return 4;
      case 8:
        return 8;
      case 16:
        return 16;
      case 32:
        return 32;
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return e & 4194240;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return e & 130023424;
      case 134217728:
        return 134217728;
      case 268435456:
        return 268435456;
      case 536870912:
        return 536870912;
      case 1073741824:
        return 1073741824;
      default:
        return e;
    }
  }
  function Yr(e, n) {
    var t = e.pendingLanes;
    if (t === 0) return 0;
    var r = 0, o = e.suspendedLanes, i = e.pingedLanes, a = t & 268435455;
    if (a !== 0) {
      var d = a & ~o;
      d !== 0 ? r = er(d) : (i &= a, i !== 0 && (r = er(i)));
    } else a = t & ~o, a !== 0 ? r = er(a) : i !== 0 && (r = er(i));
    if (r === 0) return 0;
    if (n !== 0 && n !== r && (n & o) === 0 && (o = r & -r, i = n & -n, o >= i || o === 16 && (i & 4194240) !== 0)) return n;
    if ((r & 4) !== 0 && (r |= t & 16), n = e.entangledLanes, n !== 0) for (e = e.entanglements, n &= r; 0 < n; ) t = 31 - hn(n), o = 1 << t, r |= e[t], n &= ~o;
    return r;
  }
  function Pf(e, n) {
    switch (e) {
      case 1:
      case 2:
      case 4:
        return n + 250;
      case 8:
      case 16:
      case 32:
      case 64:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return n + 5e3;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
      case 67108864:
        return -1;
      case 134217728:
      case 268435456:
      case 536870912:
      case 1073741824:
        return -1;
      default:
        return -1;
    }
  }
  function Nf(e, n) {
    for (var t = e.suspendedLanes, r = e.pingedLanes, o = e.expirationTimes, i = e.pendingLanes; 0 < i; ) {
      var a = 31 - hn(i), d = 1 << a, p = o[a];
      p === -1 ? ((d & t) === 0 || (d & r) !== 0) && (o[a] = Pf(d, n)) : p <= n && (e.expiredLanes |= d), i &= ~d;
    }
  }
  function yo(e) {
    return e = e.pendingLanes & -1073741825, e !== 0 ? e : e & 1073741824 ? 1073741824 : 0;
  }
  function Ku() {
    var e = Qr;
    return Qr <<= 1, (Qr & 4194240) === 0 && (Qr = 64), e;
  }
  function wo(e) {
    for (var n = [], t = 0; 31 > t; t++) n.push(e);
    return n;
  }
  function nr(e, n, t) {
    e.pendingLanes |= n, n !== 536870912 && (e.suspendedLanes = 0, e.pingedLanes = 0), e = e.eventTimes, n = 31 - hn(n), e[n] = t;
  }
  function zf(e, n) {
    var t = e.pendingLanes & ~n;
    e.pendingLanes = n, e.suspendedLanes = 0, e.pingedLanes = 0, e.expiredLanes &= n, e.mutableReadLanes &= n, e.entangledLanes &= n, n = e.entanglements;
    var r = e.eventTimes;
    for (e = e.expirationTimes; 0 < t; ) {
      var o = 31 - hn(t), i = 1 << o;
      n[o] = 0, r[o] = -1, e[o] = -1, t &= ~i;
    }
  }
  function ko(e, n) {
    var t = e.entangledLanes |= n;
    for (e = e.entanglements; t; ) {
      var r = 31 - hn(t), o = 1 << r;
      o & n | e[r] & n && (e[r] |= n), t &= ~o;
    }
  }
  var te = 0;
  function Yu(e) {
    return e &= -e, 1 < e ? 4 < e ? (e & 268435455) !== 0 ? 16 : 536870912 : 4 : 1;
  }
  var qu, So, Xu, Gu, Zu, Co = !1, qr = [], An = null, Un = null, Wn = null, tr = /* @__PURE__ */ new Map(), rr = /* @__PURE__ */ new Map(), Hn = [], Mf = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
  function Ju(e, n) {
    switch (e) {
      case "focusin":
      case "focusout":
        An = null;
        break;
      case "dragenter":
      case "dragleave":
        Un = null;
        break;
      case "mouseover":
      case "mouseout":
        Wn = null;
        break;
      case "pointerover":
      case "pointerout":
        tr.delete(n.pointerId);
        break;
      case "gotpointercapture":
      case "lostpointercapture":
        rr.delete(n.pointerId);
    }
  }
  function lr(e, n, t, r, o, i) {
    return e === null || e.nativeEvent !== i ? (e = { blockedOn: n, domEventName: t, eventSystemFlags: r, nativeEvent: i, targetContainers: [o] }, n !== null && (n = yr(n), n !== null && So(n)), e) : (e.eventSystemFlags |= r, n = e.targetContainers, o !== null && n.indexOf(o) === -1 && n.push(o), e);
  }
  function Tf(e, n, t, r, o) {
    switch (n) {
      case "focusin":
        return An = lr(An, e, n, t, r, o), !0;
      case "dragenter":
        return Un = lr(Un, e, n, t, r, o), !0;
      case "mouseover":
        return Wn = lr(Wn, e, n, t, r, o), !0;
      case "pointerover":
        var i = o.pointerId;
        return tr.set(i, lr(tr.get(i) || null, e, n, t, r, o)), !0;
      case "gotpointercapture":
        return i = o.pointerId, rr.set(i, lr(rr.get(i) || null, e, n, t, r, o)), !0;
    }
    return !1;
  }
  function bu(e) {
    var n = ut(e.target);
    if (n !== null) {
      var t = it(n);
      if (t !== null) {
        if (n = t.tag, n === 13) {
          if (n = Au(t), n !== null) {
            e.blockedOn = n, Zu(e.priority, function() {
              Xu(t);
            });
            return;
          }
        } else if (n === 3 && t.stateNode.current.memoizedState.isDehydrated) {
          e.blockedOn = t.tag === 3 ? t.stateNode.containerInfo : null;
          return;
        }
      }
    }
    e.blockedOn = null;
  }
  function Xr(e) {
    if (e.blockedOn !== null) return !1;
    for (var n = e.targetContainers; 0 < n.length; ) {
      var t = _o(e.domEventName, e.eventSystemFlags, n[0], e.nativeEvent);
      if (t === null) {
        t = e.nativeEvent;
        var r = new t.constructor(t.type, t);
        co = r, t.target.dispatchEvent(r), co = null;
      } else return n = yr(t), n !== null && So(n), e.blockedOn = t, !1;
      n.shift();
    }
    return !0;
  }
  function es(e, n, t) {
    Xr(e) && t.delete(n);
  }
  function Lf() {
    Co = !1, An !== null && Xr(An) && (An = null), Un !== null && Xr(Un) && (Un = null), Wn !== null && Xr(Wn) && (Wn = null), tr.forEach(es), rr.forEach(es);
  }
  function or(e, n) {
    e.blockedOn === n && (e.blockedOn = null, Co || (Co = !0, u.unstable_scheduleCallback(u.unstable_NormalPriority, Lf)));
  }
  function ir(e) {
    function n(o) {
      return or(o, e);
    }
    if (0 < qr.length) {
      or(qr[0], e);
      for (var t = 1; t < qr.length; t++) {
        var r = qr[t];
        r.blockedOn === e && (r.blockedOn = null);
      }
    }
    for (An !== null && or(An, e), Un !== null && or(Un, e), Wn !== null && or(Wn, e), tr.forEach(n), rr.forEach(n), t = 0; t < Hn.length; t++) r = Hn[t], r.blockedOn === e && (r.blockedOn = null);
    for (; 0 < Hn.length && (t = Hn[0], t.blockedOn === null); ) bu(t), t.blockedOn === null && Hn.shift();
  }
  var Pt = we.ReactCurrentBatchConfig, Gr = !0;
  function Rf(e, n, t, r) {
    var o = te, i = Pt.transition;
    Pt.transition = null;
    try {
      te = 1, Eo(e, n, t, r);
    } finally {
      te = o, Pt.transition = i;
    }
  }
  function Df(e, n, t, r) {
    var o = te, i = Pt.transition;
    Pt.transition = null;
    try {
      te = 4, Eo(e, n, t, r);
    } finally {
      te = o, Pt.transition = i;
    }
  }
  function Eo(e, n, t, r) {
    if (Gr) {
      var o = _o(e, n, t, r);
      if (o === null) Ho(e, n, r, Zr, t), Ju(e, r);
      else if (Tf(o, e, n, t, r)) r.stopPropagation();
      else if (Ju(e, r), n & 4 && -1 < Mf.indexOf(e)) {
        for (; o !== null; ) {
          var i = yr(o);
          if (i !== null && qu(i), i = _o(e, n, t, r), i === null && Ho(e, n, r, Zr, t), i === o) break;
          o = i;
        }
        o !== null && r.stopPropagation();
      } else Ho(e, n, r, null, t);
    }
  }
  var Zr = null;
  function _o(e, n, t, r) {
    if (Zr = null, e = fo(r), e = ut(e), e !== null) if (n = it(e), n === null) e = null;
    else if (t = n.tag, t === 13) {
      if (e = Au(n), e !== null) return e;
      e = null;
    } else if (t === 3) {
      if (n.stateNode.current.memoizedState.isDehydrated) return n.tag === 3 ? n.stateNode.containerInfo : null;
      e = null;
    } else n !== e && (e = null);
    return Zr = e, null;
  }
  function ns(e) {
    switch (e) {
      case "cancel":
      case "click":
      case "close":
      case "contextmenu":
      case "copy":
      case "cut":
      case "auxclick":
      case "dblclick":
      case "dragend":
      case "dragstart":
      case "drop":
      case "focusin":
      case "focusout":
      case "input":
      case "invalid":
      case "keydown":
      case "keypress":
      case "keyup":
      case "mousedown":
      case "mouseup":
      case "paste":
      case "pause":
      case "play":
      case "pointercancel":
      case "pointerdown":
      case "pointerup":
      case "ratechange":
      case "reset":
      case "resize":
      case "seeked":
      case "submit":
      case "touchcancel":
      case "touchend":
      case "touchstart":
      case "volumechange":
      case "change":
      case "selectionchange":
      case "textInput":
      case "compositionstart":
      case "compositionend":
      case "compositionupdate":
      case "beforeblur":
      case "afterblur":
      case "beforeinput":
      case "blur":
      case "fullscreenchange":
      case "focus":
      case "hashchange":
      case "popstate":
      case "select":
      case "selectstart":
        return 1;
      case "drag":
      case "dragenter":
      case "dragexit":
      case "dragleave":
      case "dragover":
      case "mousemove":
      case "mouseout":
      case "mouseover":
      case "pointermove":
      case "pointerout":
      case "pointerover":
      case "scroll":
      case "toggle":
      case "touchmove":
      case "wheel":
      case "mouseenter":
      case "mouseleave":
      case "pointerenter":
      case "pointerleave":
        return 4;
      case "message":
        switch (kf()) {
          case go:
            return 1;
          case $u:
            return 4;
          case Vr:
          case Sf:
            return 16;
          case Qu:
            return 536870912;
          default:
            return 16;
        }
      default:
        return 16;
    }
  }
  var Bn = null, xo = null, Jr = null;
  function ts() {
    if (Jr) return Jr;
    var e, n = xo, t = n.length, r, o = "value" in Bn ? Bn.value : Bn.textContent, i = o.length;
    for (e = 0; e < t && n[e] === o[e]; e++) ;
    var a = t - e;
    for (r = 1; r <= a && n[t - r] === o[i - r]; r++) ;
    return Jr = o.slice(e, 1 < r ? 1 - r : void 0);
  }
  function br(e) {
    var n = e.keyCode;
    return "charCode" in e ? (e = e.charCode, e === 0 && n === 13 && (e = 13)) : e = n, e === 10 && (e = 13), 32 <= e || e === 13 ? e : 0;
  }
  function el() {
    return !0;
  }
  function rs() {
    return !1;
  }
  function en(e) {
    function n(t, r, o, i, a) {
      this._reactName = t, this._targetInst = o, this.type = r, this.nativeEvent = i, this.target = a, this.currentTarget = null;
      for (var d in e) e.hasOwnProperty(d) && (t = e[d], this[d] = t ? t(i) : i[d]);
      return this.isDefaultPrevented = (i.defaultPrevented != null ? i.defaultPrevented : i.returnValue === !1) ? el : rs, this.isPropagationStopped = rs, this;
    }
    return D(n.prototype, { preventDefault: function() {
      this.defaultPrevented = !0;
      var t = this.nativeEvent;
      t && (t.preventDefault ? t.preventDefault() : typeof t.returnValue != "unknown" && (t.returnValue = !1), this.isDefaultPrevented = el);
    }, stopPropagation: function() {
      var t = this.nativeEvent;
      t && (t.stopPropagation ? t.stopPropagation() : typeof t.cancelBubble != "unknown" && (t.cancelBubble = !0), this.isPropagationStopped = el);
    }, persist: function() {
    }, isPersistent: el }), n;
  }
  var Nt = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(e) {
    return e.timeStamp || Date.now();
  }, defaultPrevented: 0, isTrusted: 0 }, Po = en(Nt), ur = D({}, Nt, { view: 0, detail: 0 }), Of = en(ur), No, zo, sr, nl = D({}, ur, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: To, button: 0, buttons: 0, relatedTarget: function(e) {
    return e.relatedTarget === void 0 ? e.fromElement === e.srcElement ? e.toElement : e.fromElement : e.relatedTarget;
  }, movementX: function(e) {
    return "movementX" in e ? e.movementX : (e !== sr && (sr && e.type === "mousemove" ? (No = e.screenX - sr.screenX, zo = e.screenY - sr.screenY) : zo = No = 0, sr = e), No);
  }, movementY: function(e) {
    return "movementY" in e ? e.movementY : zo;
  } }), ls = en(nl), If = D({}, nl, { dataTransfer: 0 }), Ff = en(If), jf = D({}, ur, { relatedTarget: 0 }), Mo = en(jf), Af = D({}, Nt, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), Uf = en(Af), Wf = D({}, Nt, { clipboardData: function(e) {
    return "clipboardData" in e ? e.clipboardData : window.clipboardData;
  } }), Hf = en(Wf), Bf = D({}, Nt, { data: 0 }), os = en(Bf), Vf = {
    Esc: "Escape",
    Spacebar: " ",
    Left: "ArrowLeft",
    Up: "ArrowUp",
    Right: "ArrowRight",
    Down: "ArrowDown",
    Del: "Delete",
    Win: "OS",
    Menu: "ContextMenu",
    Apps: "ContextMenu",
    Scroll: "ScrollLock",
    MozPrintableKey: "Unidentified"
  }, $f = {
    8: "Backspace",
    9: "Tab",
    12: "Clear",
    13: "Enter",
    16: "Shift",
    17: "Control",
    18: "Alt",
    19: "Pause",
    20: "CapsLock",
    27: "Escape",
    32: " ",
    33: "PageUp",
    34: "PageDown",
    35: "End",
    36: "Home",
    37: "ArrowLeft",
    38: "ArrowUp",
    39: "ArrowRight",
    40: "ArrowDown",
    45: "Insert",
    46: "Delete",
    112: "F1",
    113: "F2",
    114: "F3",
    115: "F4",
    116: "F5",
    117: "F6",
    118: "F7",
    119: "F8",
    120: "F9",
    121: "F10",
    122: "F11",
    123: "F12",
    144: "NumLock",
    145: "ScrollLock",
    224: "Meta"
  }, Qf = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
  function Kf(e) {
    var n = this.nativeEvent;
    return n.getModifierState ? n.getModifierState(e) : (e = Qf[e]) ? !!n[e] : !1;
  }
  function To() {
    return Kf;
  }
  var Yf = D({}, ur, { key: function(e) {
    if (e.key) {
      var n = Vf[e.key] || e.key;
      if (n !== "Unidentified") return n;
    }
    return e.type === "keypress" ? (e = br(e), e === 13 ? "Enter" : String.fromCharCode(e)) : e.type === "keydown" || e.type === "keyup" ? $f[e.keyCode] || "Unidentified" : "";
  }, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: To, charCode: function(e) {
    return e.type === "keypress" ? br(e) : 0;
  }, keyCode: function(e) {
    return e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
  }, which: function(e) {
    return e.type === "keypress" ? br(e) : e.type === "keydown" || e.type === "keyup" ? e.keyCode : 0;
  } }), qf = en(Yf), Xf = D({}, nl, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), is = en(Xf), Gf = D({}, ur, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: To }), Zf = en(Gf), Jf = D({}, Nt, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), bf = en(Jf), ed = D({}, nl, {
    deltaX: function(e) {
      return "deltaX" in e ? e.deltaX : "wheelDeltaX" in e ? -e.wheelDeltaX : 0;
    },
    deltaY: function(e) {
      return "deltaY" in e ? e.deltaY : "wheelDeltaY" in e ? -e.wheelDeltaY : "wheelDelta" in e ? -e.wheelDelta : 0;
    },
    deltaZ: 0,
    deltaMode: 0
  }), nd = en(ed), td = [9, 13, 27, 32], Lo = E && "CompositionEvent" in window, ar = null;
  E && "documentMode" in document && (ar = document.documentMode);
  var rd = E && "TextEvent" in window && !ar, us = E && (!Lo || ar && 8 < ar && 11 >= ar), ss = " ", as = !1;
  function cs(e, n) {
    switch (e) {
      case "keyup":
        return td.indexOf(n.keyCode) !== -1;
      case "keydown":
        return n.keyCode !== 229;
      case "keypress":
      case "mousedown":
      case "focusout":
        return !0;
      default:
        return !1;
    }
  }
  function fs(e) {
    return e = e.detail, typeof e == "object" && "data" in e ? e.data : null;
  }
  var zt = !1;
  function ld(e, n) {
    switch (e) {
      case "compositionend":
        return fs(n);
      case "keypress":
        return n.which !== 32 ? null : (as = !0, ss);
      case "textInput":
        return e = n.data, e === ss && as ? null : e;
      default:
        return null;
    }
  }
  function od(e, n) {
    if (zt) return e === "compositionend" || !Lo && cs(e, n) ? (e = ts(), Jr = xo = Bn = null, zt = !1, e) : null;
    switch (e) {
      case "paste":
        return null;
      case "keypress":
        if (!(n.ctrlKey || n.altKey || n.metaKey) || n.ctrlKey && n.altKey) {
          if (n.char && 1 < n.char.length) return n.char;
          if (n.which) return String.fromCharCode(n.which);
        }
        return null;
      case "compositionend":
        return us && n.locale !== "ko" ? null : n.data;
      default:
        return null;
    }
  }
  var id = { color: !0, date: !0, datetime: !0, "datetime-local": !0, email: !0, month: !0, number: !0, password: !0, range: !0, search: !0, tel: !0, text: !0, time: !0, url: !0, week: !0 };
  function ds(e) {
    var n = e && e.nodeName && e.nodeName.toLowerCase();
    return n === "input" ? !!id[e.type] : n === "textarea";
  }
  function ps(e, n, t, r) {
    Du(r), n = il(n, "onChange"), 0 < n.length && (t = new Po("onChange", "change", null, t, r), e.push({ event: t, listeners: n }));
  }
  var cr = null, fr = null;
  function ud(e) {
    Ls(e, 0);
  }
  function tl(e) {
    var n = Dt(e);
    if (Su(n)) return e;
  }
  function sd(e, n) {
    if (e === "change") return n;
  }
  var hs = !1;
  if (E) {
    var Ro;
    if (E) {
      var Do = "oninput" in document;
      if (!Do) {
        var ms = document.createElement("div");
        ms.setAttribute("oninput", "return;"), Do = typeof ms.oninput == "function";
      }
      Ro = Do;
    } else Ro = !1;
    hs = Ro && (!document.documentMode || 9 < document.documentMode);
  }
  function vs() {
    cr && (cr.detachEvent("onpropertychange", gs), fr = cr = null);
  }
  function gs(e) {
    if (e.propertyName === "value" && tl(fr)) {
      var n = [];
      ps(n, fr, e, fo(e)), ju(ud, n);
    }
  }
  function ad(e, n, t) {
    e === "focusin" ? (vs(), cr = n, fr = t, cr.attachEvent("onpropertychange", gs)) : e === "focusout" && vs();
  }
  function cd(e) {
    if (e === "selectionchange" || e === "keyup" || e === "keydown") return tl(fr);
  }
  function fd(e, n) {
    if (e === "click") return tl(n);
  }
  function dd(e, n) {
    if (e === "input" || e === "change") return tl(n);
  }
  function pd(e, n) {
    return e === n && (e !== 0 || 1 / e === 1 / n) || e !== e && n !== n;
  }
  var mn = typeof Object.is == "function" ? Object.is : pd;
  function dr(e, n) {
    if (mn(e, n)) return !0;
    if (typeof e != "object" || e === null || typeof n != "object" || n === null) return !1;
    var t = Object.keys(e), r = Object.keys(n);
    if (t.length !== r.length) return !1;
    for (r = 0; r < t.length; r++) {
      var o = t[r];
      if (!z.call(n, o) || !mn(e[o], n[o])) return !1;
    }
    return !0;
  }
  function ys(e) {
    for (; e && e.firstChild; ) e = e.firstChild;
    return e;
  }
  function ws(e, n) {
    var t = ys(e);
    e = 0;
    for (var r; t; ) {
      if (t.nodeType === 3) {
        if (r = e + t.textContent.length, e <= n && r >= n) return { node: t, offset: n - e };
        e = r;
      }
      e: {
        for (; t; ) {
          if (t.nextSibling) {
            t = t.nextSibling;
            break e;
          }
          t = t.parentNode;
        }
        t = void 0;
      }
      t = ys(t);
    }
  }
  function ks(e, n) {
    return e && n ? e === n ? !0 : e && e.nodeType === 3 ? !1 : n && n.nodeType === 3 ? ks(e, n.parentNode) : "contains" in e ? e.contains(n) : e.compareDocumentPosition ? !!(e.compareDocumentPosition(n) & 16) : !1 : !1;
  }
  function Ss() {
    for (var e = window, n = Ur(); n instanceof e.HTMLIFrameElement; ) {
      try {
        var t = typeof n.contentWindow.location.href == "string";
      } catch {
        t = !1;
      }
      if (t) e = n.contentWindow;
      else break;
      n = Ur(e.document);
    }
    return n;
  }
  function Oo(e) {
    var n = e && e.nodeName && e.nodeName.toLowerCase();
    return n && (n === "input" && (e.type === "text" || e.type === "search" || e.type === "tel" || e.type === "url" || e.type === "password") || n === "textarea" || e.contentEditable === "true");
  }
  function hd(e) {
    var n = Ss(), t = e.focusedElem, r = e.selectionRange;
    if (n !== t && t && t.ownerDocument && ks(t.ownerDocument.documentElement, t)) {
      if (r !== null && Oo(t)) {
        if (n = r.start, e = r.end, e === void 0 && (e = n), "selectionStart" in t) t.selectionStart = n, t.selectionEnd = Math.min(e, t.value.length);
        else if (e = (n = t.ownerDocument || document) && n.defaultView || window, e.getSelection) {
          e = e.getSelection();
          var o = t.textContent.length, i = Math.min(r.start, o);
          r = r.end === void 0 ? i : Math.min(r.end, o), !e.extend && i > r && (o = r, r = i, i = o), o = ws(t, i);
          var a = ws(
            t,
            r
          );
          o && a && (e.rangeCount !== 1 || e.anchorNode !== o.node || e.anchorOffset !== o.offset || e.focusNode !== a.node || e.focusOffset !== a.offset) && (n = n.createRange(), n.setStart(o.node, o.offset), e.removeAllRanges(), i > r ? (e.addRange(n), e.extend(a.node, a.offset)) : (n.setEnd(a.node, a.offset), e.addRange(n)));
        }
      }
      for (n = [], e = t; e = e.parentNode; ) e.nodeType === 1 && n.push({ element: e, left: e.scrollLeft, top: e.scrollTop });
      for (typeof t.focus == "function" && t.focus(), t = 0; t < n.length; t++) e = n[t], e.element.scrollLeft = e.left, e.element.scrollTop = e.top;
    }
  }
  var md = E && "documentMode" in document && 11 >= document.documentMode, Mt = null, Io = null, pr = null, Fo = !1;
  function Cs(e, n, t) {
    var r = t.window === t ? t.document : t.nodeType === 9 ? t : t.ownerDocument;
    Fo || Mt == null || Mt !== Ur(r) || (r = Mt, "selectionStart" in r && Oo(r) ? r = { start: r.selectionStart, end: r.selectionEnd } : (r = (r.ownerDocument && r.ownerDocument.defaultView || window).getSelection(), r = { anchorNode: r.anchorNode, anchorOffset: r.anchorOffset, focusNode: r.focusNode, focusOffset: r.focusOffset }), pr && dr(pr, r) || (pr = r, r = il(Io, "onSelect"), 0 < r.length && (n = new Po("onSelect", "select", null, n, t), e.push({ event: n, listeners: r }), n.target = Mt)));
  }
  function rl(e, n) {
    var t = {};
    return t[e.toLowerCase()] = n.toLowerCase(), t["Webkit" + e] = "webkit" + n, t["Moz" + e] = "moz" + n, t;
  }
  var Tt = { animationend: rl("Animation", "AnimationEnd"), animationiteration: rl("Animation", "AnimationIteration"), animationstart: rl("Animation", "AnimationStart"), transitionend: rl("Transition", "TransitionEnd") }, jo = {}, Es = {};
  E && (Es = document.createElement("div").style, "AnimationEvent" in window || (delete Tt.animationend.animation, delete Tt.animationiteration.animation, delete Tt.animationstart.animation), "TransitionEvent" in window || delete Tt.transitionend.transition);
  function ll(e) {
    if (jo[e]) return jo[e];
    if (!Tt[e]) return e;
    var n = Tt[e], t;
    for (t in n) if (n.hasOwnProperty(t) && t in Es) return jo[e] = n[t];
    return e;
  }
  var _s = ll("animationend"), xs = ll("animationiteration"), Ps = ll("animationstart"), Ns = ll("transitionend"), zs = /* @__PURE__ */ new Map(), Ms = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
  function Vn(e, n) {
    zs.set(e, n), m(n, [e]);
  }
  for (var Ao = 0; Ao < Ms.length; Ao++) {
    var Uo = Ms[Ao], vd = Uo.toLowerCase(), gd = Uo[0].toUpperCase() + Uo.slice(1);
    Vn(vd, "on" + gd);
  }
  Vn(_s, "onAnimationEnd"), Vn(xs, "onAnimationIteration"), Vn(Ps, "onAnimationStart"), Vn("dblclick", "onDoubleClick"), Vn("focusin", "onFocus"), Vn("focusout", "onBlur"), Vn(Ns, "onTransitionEnd"), k("onMouseEnter", ["mouseout", "mouseover"]), k("onMouseLeave", ["mouseout", "mouseover"]), k("onPointerEnter", ["pointerout", "pointerover"]), k("onPointerLeave", ["pointerout", "pointerover"]), m("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" ")), m("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")), m("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]), m("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" ")), m("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" ")), m("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
  var hr = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), yd = new Set("cancel close invalid load scroll toggle".split(" ").concat(hr));
  function Ts(e, n, t) {
    var r = e.type || "unknown-event";
    e.currentTarget = t, vf(r, n, void 0, e), e.currentTarget = null;
  }
  function Ls(e, n) {
    n = (n & 4) !== 0;
    for (var t = 0; t < e.length; t++) {
      var r = e[t], o = r.event;
      r = r.listeners;
      e: {
        var i = void 0;
        if (n) for (var a = r.length - 1; 0 <= a; a--) {
          var d = r[a], p = d.instance, w = d.currentTarget;
          if (d = d.listener, p !== i && o.isPropagationStopped()) break e;
          Ts(o, d, w), i = p;
        }
        else for (a = 0; a < r.length; a++) {
          if (d = r[a], p = d.instance, w = d.currentTarget, d = d.listener, p !== i && o.isPropagationStopped()) break e;
          Ts(o, d, w), i = p;
        }
      }
    }
    if (Br) throw e = vo, Br = !1, vo = null, e;
  }
  function oe(e, n) {
    var t = n[Yo];
    t === void 0 && (t = n[Yo] = /* @__PURE__ */ new Set());
    var r = e + "__bubble";
    t.has(r) || (Rs(n, e, 2, !1), t.add(r));
  }
  function Wo(e, n, t) {
    var r = 0;
    n && (r |= 4), Rs(t, e, r, n);
  }
  var ol = "_reactListening" + Math.random().toString(36).slice(2);
  function mr(e) {
    if (!e[ol]) {
      e[ol] = !0, c.forEach(function(t) {
        t !== "selectionchange" && (yd.has(t) || Wo(t, !1, e), Wo(t, !0, e));
      });
      var n = e.nodeType === 9 ? e : e.ownerDocument;
      n === null || n[ol] || (n[ol] = !0, Wo("selectionchange", !1, n));
    }
  }
  function Rs(e, n, t, r) {
    switch (ns(n)) {
      case 1:
        var o = Rf;
        break;
      case 4:
        o = Df;
        break;
      default:
        o = Eo;
    }
    t = o.bind(null, n, t, e), o = void 0, !mo || n !== "touchstart" && n !== "touchmove" && n !== "wheel" || (o = !0), r ? o !== void 0 ? e.addEventListener(n, t, { capture: !0, passive: o }) : e.addEventListener(n, t, !0) : o !== void 0 ? e.addEventListener(n, t, { passive: o }) : e.addEventListener(n, t, !1);
  }
  function Ho(e, n, t, r, o) {
    var i = r;
    if ((n & 1) === 0 && (n & 2) === 0 && r !== null) e: for (; ; ) {
      if (r === null) return;
      var a = r.tag;
      if (a === 3 || a === 4) {
        var d = r.stateNode.containerInfo;
        if (d === o || d.nodeType === 8 && d.parentNode === o) break;
        if (a === 4) for (a = r.return; a !== null; ) {
          var p = a.tag;
          if ((p === 3 || p === 4) && (p = a.stateNode.containerInfo, p === o || p.nodeType === 8 && p.parentNode === o)) return;
          a = a.return;
        }
        for (; d !== null; ) {
          if (a = ut(d), a === null) return;
          if (p = a.tag, p === 5 || p === 6) {
            r = i = a;
            continue e;
          }
          d = d.parentNode;
        }
      }
      r = r.return;
    }
    ju(function() {
      var w = i, x = fo(t), P = [];
      e: {
        var C = zs.get(e);
        if (C !== void 0) {
          var L = Po, I = e;
          switch (e) {
            case "keypress":
              if (br(t) === 0) break e;
            case "keydown":
            case "keyup":
              L = qf;
              break;
            case "focusin":
              I = "focus", L = Mo;
              break;
            case "focusout":
              I = "blur", L = Mo;
              break;
            case "beforeblur":
            case "afterblur":
              L = Mo;
              break;
            case "click":
              if (t.button === 2) break e;
            case "auxclick":
            case "dblclick":
            case "mousedown":
            case "mousemove":
            case "mouseup":
            case "mouseout":
            case "mouseover":
            case "contextmenu":
              L = ls;
              break;
            case "drag":
            case "dragend":
            case "dragenter":
            case "dragexit":
            case "dragleave":
            case "dragover":
            case "dragstart":
            case "drop":
              L = Ff;
              break;
            case "touchcancel":
            case "touchend":
            case "touchmove":
            case "touchstart":
              L = Zf;
              break;
            case _s:
            case xs:
            case Ps:
              L = Uf;
              break;
            case Ns:
              L = bf;
              break;
            case "scroll":
              L = Of;
              break;
            case "wheel":
              L = nd;
              break;
            case "copy":
            case "cut":
            case "paste":
              L = Hf;
              break;
            case "gotpointercapture":
            case "lostpointercapture":
            case "pointercancel":
            case "pointerdown":
            case "pointermove":
            case "pointerout":
            case "pointerover":
            case "pointerup":
              L = is;
          }
          var F = (n & 4) !== 0, ye = !F && e === "scroll", g = F ? C !== null ? C + "Capture" : null : C;
          F = [];
          for (var h = w, y; h !== null; ) {
            y = h;
            var N = y.stateNode;
            if (y.tag === 5 && N !== null && (y = N, g !== null && (N = Zt(h, g), N != null && F.push(vr(h, N, y)))), ye) break;
            h = h.return;
          }
          0 < F.length && (C = new L(C, I, null, t, x), P.push({ event: C, listeners: F }));
        }
      }
      if ((n & 7) === 0) {
        e: {
          if (C = e === "mouseover" || e === "pointerover", L = e === "mouseout" || e === "pointerout", C && t !== co && (I = t.relatedTarget || t.fromElement) && (ut(I) || I[zn])) break e;
          if ((L || C) && (C = x.window === x ? x : (C = x.ownerDocument) ? C.defaultView || C.parentWindow : window, L ? (I = t.relatedTarget || t.toElement, L = w, I = I ? ut(I) : null, I !== null && (ye = it(I), I !== ye || I.tag !== 5 && I.tag !== 6) && (I = null)) : (L = null, I = w), L !== I)) {
            if (F = ls, N = "onMouseLeave", g = "onMouseEnter", h = "mouse", (e === "pointerout" || e === "pointerover") && (F = is, N = "onPointerLeave", g = "onPointerEnter", h = "pointer"), ye = L == null ? C : Dt(L), y = I == null ? C : Dt(I), C = new F(N, h + "leave", L, t, x), C.target = ye, C.relatedTarget = y, N = null, ut(x) === w && (F = new F(g, h + "enter", I, t, x), F.target = y, F.relatedTarget = ye, N = F), ye = N, L && I) n: {
              for (F = L, g = I, h = 0, y = F; y; y = Lt(y)) h++;
              for (y = 0, N = g; N; N = Lt(N)) y++;
              for (; 0 < h - y; ) F = Lt(F), h--;
              for (; 0 < y - h; ) g = Lt(g), y--;
              for (; h--; ) {
                if (F === g || g !== null && F === g.alternate) break n;
                F = Lt(F), g = Lt(g);
              }
              F = null;
            }
            else F = null;
            L !== null && Ds(P, C, L, F, !1), I !== null && ye !== null && Ds(P, ye, I, F, !0);
          }
        }
        e: {
          if (C = w ? Dt(w) : window, L = C.nodeName && C.nodeName.toLowerCase(), L === "select" || L === "input" && C.type === "file") var A = sd;
          else if (ds(C)) if (hs) A = dd;
          else {
            A = cd;
            var U = ad;
          }
          else (L = C.nodeName) && L.toLowerCase() === "input" && (C.type === "checkbox" || C.type === "radio") && (A = fd);
          if (A && (A = A(e, w))) {
            ps(P, A, t, x);
            break e;
          }
          U && U(e, C, w), e === "focusout" && (U = C._wrapperState) && U.controlled && C.type === "number" && oo(C, "number", C.value);
        }
        switch (U = w ? Dt(w) : window, e) {
          case "focusin":
            (ds(U) || U.contentEditable === "true") && (Mt = U, Io = w, pr = null);
            break;
          case "focusout":
            pr = Io = Mt = null;
            break;
          case "mousedown":
            Fo = !0;
            break;
          case "contextmenu":
          case "mouseup":
          case "dragend":
            Fo = !1, Cs(P, t, x);
            break;
          case "selectionchange":
            if (md) break;
          case "keydown":
          case "keyup":
            Cs(P, t, x);
        }
        var W;
        if (Lo) e: {
          switch (e) {
            case "compositionstart":
              var V = "onCompositionStart";
              break e;
            case "compositionend":
              V = "onCompositionEnd";
              break e;
            case "compositionupdate":
              V = "onCompositionUpdate";
              break e;
          }
          V = void 0;
        }
        else zt ? cs(e, t) && (V = "onCompositionEnd") : e === "keydown" && t.keyCode === 229 && (V = "onCompositionStart");
        V && (us && t.locale !== "ko" && (zt || V !== "onCompositionStart" ? V === "onCompositionEnd" && zt && (W = ts()) : (Bn = x, xo = "value" in Bn ? Bn.value : Bn.textContent, zt = !0)), U = il(w, V), 0 < U.length && (V = new os(V, e, null, t, x), P.push({ event: V, listeners: U }), W ? V.data = W : (W = fs(t), W !== null && (V.data = W)))), (W = rd ? ld(e, t) : od(e, t)) && (w = il(w, "onBeforeInput"), 0 < w.length && (x = new os("onBeforeInput", "beforeinput", null, t, x), P.push({ event: x, listeners: w }), x.data = W));
      }
      Ls(P, n);
    });
  }
  function vr(e, n, t) {
    return { instance: e, listener: n, currentTarget: t };
  }
  function il(e, n) {
    for (var t = n + "Capture", r = []; e !== null; ) {
      var o = e, i = o.stateNode;
      o.tag === 5 && i !== null && (o = i, i = Zt(e, t), i != null && r.unshift(vr(e, i, o)), i = Zt(e, n), i != null && r.push(vr(e, i, o))), e = e.return;
    }
    return r;
  }
  function Lt(e) {
    if (e === null) return null;
    do
      e = e.return;
    while (e && e.tag !== 5);
    return e || null;
  }
  function Ds(e, n, t, r, o) {
    for (var i = n._reactName, a = []; t !== null && t !== r; ) {
      var d = t, p = d.alternate, w = d.stateNode;
      if (p !== null && p === r) break;
      d.tag === 5 && w !== null && (d = w, o ? (p = Zt(t, i), p != null && a.unshift(vr(t, p, d))) : o || (p = Zt(t, i), p != null && a.push(vr(t, p, d)))), t = t.return;
    }
    a.length !== 0 && e.push({ event: n, listeners: a });
  }
  var wd = /\r\n?/g, kd = /\u0000|\uFFFD/g;
  function Os(e) {
    return (typeof e == "string" ? e : "" + e).replace(wd, `
`).replace(kd, "");
  }
  function ul(e, n, t) {
    if (n = Os(n), Os(e) !== n && t) throw Error(s(425));
  }
  function sl() {
  }
  var Bo = null, Vo = null;
  function $o(e, n) {
    return e === "textarea" || e === "noscript" || typeof n.children == "string" || typeof n.children == "number" || typeof n.dangerouslySetInnerHTML == "object" && n.dangerouslySetInnerHTML !== null && n.dangerouslySetInnerHTML.__html != null;
  }
  var Qo = typeof setTimeout == "function" ? setTimeout : void 0, Sd = typeof clearTimeout == "function" ? clearTimeout : void 0, Is = typeof Promise == "function" ? Promise : void 0, Cd = typeof queueMicrotask == "function" ? queueMicrotask : typeof Is < "u" ? function(e) {
    return Is.resolve(null).then(e).catch(Ed);
  } : Qo;
  function Ed(e) {
    setTimeout(function() {
      throw e;
    });
  }
  function Ko(e, n) {
    var t = n, r = 0;
    do {
      var o = t.nextSibling;
      if (e.removeChild(t), o && o.nodeType === 8) if (t = o.data, t === "/$") {
        if (r === 0) {
          e.removeChild(o), ir(n);
          return;
        }
        r--;
      } else t !== "$" && t !== "$?" && t !== "$!" || r++;
      t = o;
    } while (t);
    ir(n);
  }
  function $n(e) {
    for (; e != null; e = e.nextSibling) {
      var n = e.nodeType;
      if (n === 1 || n === 3) break;
      if (n === 8) {
        if (n = e.data, n === "$" || n === "$!" || n === "$?") break;
        if (n === "/$") return null;
      }
    }
    return e;
  }
  function Fs(e) {
    e = e.previousSibling;
    for (var n = 0; e; ) {
      if (e.nodeType === 8) {
        var t = e.data;
        if (t === "$" || t === "$!" || t === "$?") {
          if (n === 0) return e;
          n--;
        } else t === "/$" && n++;
      }
      e = e.previousSibling;
    }
    return null;
  }
  var Rt = Math.random().toString(36).slice(2), En = "__reactFiber$" + Rt, gr = "__reactProps$" + Rt, zn = "__reactContainer$" + Rt, Yo = "__reactEvents$" + Rt, _d = "__reactListeners$" + Rt, xd = "__reactHandles$" + Rt;
  function ut(e) {
    var n = e[En];
    if (n) return n;
    for (var t = e.parentNode; t; ) {
      if (n = t[zn] || t[En]) {
        if (t = n.alternate, n.child !== null || t !== null && t.child !== null) for (e = Fs(e); e !== null; ) {
          if (t = e[En]) return t;
          e = Fs(e);
        }
        return n;
      }
      e = t, t = e.parentNode;
    }
    return null;
  }
  function yr(e) {
    return e = e[En] || e[zn], !e || e.tag !== 5 && e.tag !== 6 && e.tag !== 13 && e.tag !== 3 ? null : e;
  }
  function Dt(e) {
    if (e.tag === 5 || e.tag === 6) return e.stateNode;
    throw Error(s(33));
  }
  function al(e) {
    return e[gr] || null;
  }
  var qo = [], Ot = -1;
  function Qn(e) {
    return { current: e };
  }
  function ie(e) {
    0 > Ot || (e.current = qo[Ot], qo[Ot] = null, Ot--);
  }
  function le(e, n) {
    Ot++, qo[Ot] = e.current, e.current = n;
  }
  var Kn = {}, Oe = Qn(Kn), $e = Qn(!1), st = Kn;
  function It(e, n) {
    var t = e.type.contextTypes;
    if (!t) return Kn;
    var r = e.stateNode;
    if (r && r.__reactInternalMemoizedUnmaskedChildContext === n) return r.__reactInternalMemoizedMaskedChildContext;
    var o = {}, i;
    for (i in t) o[i] = n[i];
    return r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = n, e.__reactInternalMemoizedMaskedChildContext = o), o;
  }
  function Qe(e) {
    return e = e.childContextTypes, e != null;
  }
  function cl() {
    ie($e), ie(Oe);
  }
  function js(e, n, t) {
    if (Oe.current !== Kn) throw Error(s(168));
    le(Oe, n), le($e, t);
  }
  function As(e, n, t) {
    var r = e.stateNode;
    if (n = n.childContextTypes, typeof r.getChildContext != "function") return t;
    r = r.getChildContext();
    for (var o in r) if (!(o in n)) throw Error(s(108, re(e) || "Unknown", o));
    return D({}, t, r);
  }
  function fl(e) {
    return e = (e = e.stateNode) && e.__reactInternalMemoizedMergedChildContext || Kn, st = Oe.current, le(Oe, e), le($e, $e.current), !0;
  }
  function Us(e, n, t) {
    var r = e.stateNode;
    if (!r) throw Error(s(169));
    t ? (e = As(e, n, st), r.__reactInternalMemoizedMergedChildContext = e, ie($e), ie(Oe), le(Oe, e)) : ie($e), le($e, t);
  }
  var Mn = null, dl = !1, Xo = !1;
  function Ws(e) {
    Mn === null ? Mn = [e] : Mn.push(e);
  }
  function Pd(e) {
    dl = !0, Ws(e);
  }
  function Yn() {
    if (!Xo && Mn !== null) {
      Xo = !0;
      var e = 0, n = te;
      try {
        var t = Mn;
        for (te = 1; e < t.length; e++) {
          var r = t[e];
          do
            r = r(!0);
          while (r !== null);
        }
        Mn = null, dl = !1;
      } catch (o) {
        throw Mn !== null && (Mn = Mn.slice(e + 1)), Bu(go, Yn), o;
      } finally {
        te = n, Xo = !1;
      }
    }
    return null;
  }
  var Ft = [], jt = 0, pl = null, hl = 0, ln = [], on = 0, at = null, Tn = 1, Ln = "";
  function ct(e, n) {
    Ft[jt++] = hl, Ft[jt++] = pl, pl = e, hl = n;
  }
  function Hs(e, n, t) {
    ln[on++] = Tn, ln[on++] = Ln, ln[on++] = at, at = e;
    var r = Tn;
    e = Ln;
    var o = 32 - hn(r) - 1;
    r &= ~(1 << o), t += 1;
    var i = 32 - hn(n) + o;
    if (30 < i) {
      var a = o - o % 5;
      i = (r & (1 << a) - 1).toString(32), r >>= a, o -= a, Tn = 1 << 32 - hn(n) + o | t << o | r, Ln = i + e;
    } else Tn = 1 << i | t << o | r, Ln = e;
  }
  function Go(e) {
    e.return !== null && (ct(e, 1), Hs(e, 1, 0));
  }
  function Zo(e) {
    for (; e === pl; ) pl = Ft[--jt], Ft[jt] = null, hl = Ft[--jt], Ft[jt] = null;
    for (; e === at; ) at = ln[--on], ln[on] = null, Ln = ln[--on], ln[on] = null, Tn = ln[--on], ln[on] = null;
  }
  var nn = null, tn = null, ae = !1, vn = null;
  function Bs(e, n) {
    var t = cn(5, null, null, 0);
    t.elementType = "DELETED", t.stateNode = n, t.return = e, n = e.deletions, n === null ? (e.deletions = [t], e.flags |= 16) : n.push(t);
  }
  function Vs(e, n) {
    switch (e.tag) {
      case 5:
        var t = e.type;
        return n = n.nodeType !== 1 || t.toLowerCase() !== n.nodeName.toLowerCase() ? null : n, n !== null ? (e.stateNode = n, nn = e, tn = $n(n.firstChild), !0) : !1;
      case 6:
        return n = e.pendingProps === "" || n.nodeType !== 3 ? null : n, n !== null ? (e.stateNode = n, nn = e, tn = null, !0) : !1;
      case 13:
        return n = n.nodeType !== 8 ? null : n, n !== null ? (t = at !== null ? { id: Tn, overflow: Ln } : null, e.memoizedState = { dehydrated: n, treeContext: t, retryLane: 1073741824 }, t = cn(18, null, null, 0), t.stateNode = n, t.return = e, e.child = t, nn = e, tn = null, !0) : !1;
      default:
        return !1;
    }
  }
  function Jo(e) {
    return (e.mode & 1) !== 0 && (e.flags & 128) === 0;
  }
  function bo(e) {
    if (ae) {
      var n = tn;
      if (n) {
        var t = n;
        if (!Vs(e, n)) {
          if (Jo(e)) throw Error(s(418));
          n = $n(t.nextSibling);
          var r = nn;
          n && Vs(e, n) ? Bs(r, t) : (e.flags = e.flags & -4097 | 2, ae = !1, nn = e);
        }
      } else {
        if (Jo(e)) throw Error(s(418));
        e.flags = e.flags & -4097 | 2, ae = !1, nn = e;
      }
    }
  }
  function $s(e) {
    for (e = e.return; e !== null && e.tag !== 5 && e.tag !== 3 && e.tag !== 13; ) e = e.return;
    nn = e;
  }
  function ml(e) {
    if (e !== nn) return !1;
    if (!ae) return $s(e), ae = !0, !1;
    var n;
    if ((n = e.tag !== 3) && !(n = e.tag !== 5) && (n = e.type, n = n !== "head" && n !== "body" && !$o(e.type, e.memoizedProps)), n && (n = tn)) {
      if (Jo(e)) throw Qs(), Error(s(418));
      for (; n; ) Bs(e, n), n = $n(n.nextSibling);
    }
    if ($s(e), e.tag === 13) {
      if (e = e.memoizedState, e = e !== null ? e.dehydrated : null, !e) throw Error(s(317));
      e: {
        for (e = e.nextSibling, n = 0; e; ) {
          if (e.nodeType === 8) {
            var t = e.data;
            if (t === "/$") {
              if (n === 0) {
                tn = $n(e.nextSibling);
                break e;
              }
              n--;
            } else t !== "$" && t !== "$!" && t !== "$?" || n++;
          }
          e = e.nextSibling;
        }
        tn = null;
      }
    } else tn = nn ? $n(e.stateNode.nextSibling) : null;
    return !0;
  }
  function Qs() {
    for (var e = tn; e; ) e = $n(e.nextSibling);
  }
  function At() {
    tn = nn = null, ae = !1;
  }
  function ei(e) {
    vn === null ? vn = [e] : vn.push(e);
  }
  var Nd = we.ReactCurrentBatchConfig;
  function wr(e, n, t) {
    if (e = t.ref, e !== null && typeof e != "function" && typeof e != "object") {
      if (t._owner) {
        if (t = t._owner, t) {
          if (t.tag !== 1) throw Error(s(309));
          var r = t.stateNode;
        }
        if (!r) throw Error(s(147, e));
        var o = r, i = "" + e;
        return n !== null && n.ref !== null && typeof n.ref == "function" && n.ref._stringRef === i ? n.ref : (n = function(a) {
          var d = o.refs;
          a === null ? delete d[i] : d[i] = a;
        }, n._stringRef = i, n);
      }
      if (typeof e != "string") throw Error(s(284));
      if (!t._owner) throw Error(s(290, e));
    }
    return e;
  }
  function vl(e, n) {
    throw e = Object.prototype.toString.call(n), Error(s(31, e === "[object Object]" ? "object with keys {" + Object.keys(n).join(", ") + "}" : e));
  }
  function Ks(e) {
    var n = e._init;
    return n(e._payload);
  }
  function Ys(e) {
    function n(g, h) {
      if (e) {
        var y = g.deletions;
        y === null ? (g.deletions = [h], g.flags |= 16) : y.push(h);
      }
    }
    function t(g, h) {
      if (!e) return null;
      for (; h !== null; ) n(g, h), h = h.sibling;
      return null;
    }
    function r(g, h) {
      for (g = /* @__PURE__ */ new Map(); h !== null; ) h.key !== null ? g.set(h.key, h) : g.set(h.index, h), h = h.sibling;
      return g;
    }
    function o(g, h) {
      return g = nt(g, h), g.index = 0, g.sibling = null, g;
    }
    function i(g, h, y) {
      return g.index = y, e ? (y = g.alternate, y !== null ? (y = y.index, y < h ? (g.flags |= 2, h) : y) : (g.flags |= 2, h)) : (g.flags |= 1048576, h);
    }
    function a(g) {
      return e && g.alternate === null && (g.flags |= 2), g;
    }
    function d(g, h, y, N) {
      return h === null || h.tag !== 6 ? (h = Qi(y, g.mode, N), h.return = g, h) : (h = o(h, y), h.return = g, h);
    }
    function p(g, h, y, N) {
      var A = y.type;
      return A === Ee ? x(g, h, y.props.children, N, y.key) : h !== null && (h.elementType === A || typeof A == "object" && A !== null && A.$$typeof === Ve && Ks(A) === h.type) ? (N = o(h, y.props), N.ref = wr(g, h, y), N.return = g, N) : (N = Wl(y.type, y.key, y.props, null, g.mode, N), N.ref = wr(g, h, y), N.return = g, N);
    }
    function w(g, h, y, N) {
      return h === null || h.tag !== 4 || h.stateNode.containerInfo !== y.containerInfo || h.stateNode.implementation !== y.implementation ? (h = Ki(y, g.mode, N), h.return = g, h) : (h = o(h, y.children || []), h.return = g, h);
    }
    function x(g, h, y, N, A) {
      return h === null || h.tag !== 7 ? (h = yt(y, g.mode, N, A), h.return = g, h) : (h = o(h, y), h.return = g, h);
    }
    function P(g, h, y) {
      if (typeof h == "string" && h !== "" || typeof h == "number") return h = Qi("" + h, g.mode, y), h.return = g, h;
      if (typeof h == "object" && h !== null) {
        switch (h.$$typeof) {
          case pe:
            return y = Wl(h.type, h.key, h.props, null, g.mode, y), y.ref = wr(g, null, h), y.return = g, y;
          case Ce:
            return h = Ki(h, g.mode, y), h.return = g, h;
          case Ve:
            var N = h._init;
            return P(g, N(h._payload), y);
        }
        if (qt(h) || H(h)) return h = yt(h, g.mode, y, null), h.return = g, h;
        vl(g, h);
      }
      return null;
    }
    function C(g, h, y, N) {
      var A = h !== null ? h.key : null;
      if (typeof y == "string" && y !== "" || typeof y == "number") return A !== null ? null : d(g, h, "" + y, N);
      if (typeof y == "object" && y !== null) {
        switch (y.$$typeof) {
          case pe:
            return y.key === A ? p(g, h, y, N) : null;
          case Ce:
            return y.key === A ? w(g, h, y, N) : null;
          case Ve:
            return A = y._init, C(
              g,
              h,
              A(y._payload),
              N
            );
        }
        if (qt(y) || H(y)) return A !== null ? null : x(g, h, y, N, null);
        vl(g, y);
      }
      return null;
    }
    function L(g, h, y, N, A) {
      if (typeof N == "string" && N !== "" || typeof N == "number") return g = g.get(y) || null, d(h, g, "" + N, A);
      if (typeof N == "object" && N !== null) {
        switch (N.$$typeof) {
          case pe:
            return g = g.get(N.key === null ? y : N.key) || null, p(h, g, N, A);
          case Ce:
            return g = g.get(N.key === null ? y : N.key) || null, w(h, g, N, A);
          case Ve:
            var U = N._init;
            return L(g, h, y, U(N._payload), A);
        }
        if (qt(N) || H(N)) return g = g.get(y) || null, x(h, g, N, A, null);
        vl(h, N);
      }
      return null;
    }
    function I(g, h, y, N) {
      for (var A = null, U = null, W = h, V = h = 0, Te = null; W !== null && V < y.length; V++) {
        W.index > V ? (Te = W, W = null) : Te = W.sibling;
        var ee = C(g, W, y[V], N);
        if (ee === null) {
          W === null && (W = Te);
          break;
        }
        e && W && ee.alternate === null && n(g, W), h = i(ee, h, V), U === null ? A = ee : U.sibling = ee, U = ee, W = Te;
      }
      if (V === y.length) return t(g, W), ae && ct(g, V), A;
      if (W === null) {
        for (; V < y.length; V++) W = P(g, y[V], N), W !== null && (h = i(W, h, V), U === null ? A = W : U.sibling = W, U = W);
        return ae && ct(g, V), A;
      }
      for (W = r(g, W); V < y.length; V++) Te = L(W, g, V, y[V], N), Te !== null && (e && Te.alternate !== null && W.delete(Te.key === null ? V : Te.key), h = i(Te, h, V), U === null ? A = Te : U.sibling = Te, U = Te);
      return e && W.forEach(function(tt) {
        return n(g, tt);
      }), ae && ct(g, V), A;
    }
    function F(g, h, y, N) {
      var A = H(y);
      if (typeof A != "function") throw Error(s(150));
      if (y = A.call(y), y == null) throw Error(s(151));
      for (var U = A = null, W = h, V = h = 0, Te = null, ee = y.next(); W !== null && !ee.done; V++, ee = y.next()) {
        W.index > V ? (Te = W, W = null) : Te = W.sibling;
        var tt = C(g, W, ee.value, N);
        if (tt === null) {
          W === null && (W = Te);
          break;
        }
        e && W && tt.alternate === null && n(g, W), h = i(tt, h, V), U === null ? A = tt : U.sibling = tt, U = tt, W = Te;
      }
      if (ee.done) return t(
        g,
        W
      ), ae && ct(g, V), A;
      if (W === null) {
        for (; !ee.done; V++, ee = y.next()) ee = P(g, ee.value, N), ee !== null && (h = i(ee, h, V), U === null ? A = ee : U.sibling = ee, U = ee);
        return ae && ct(g, V), A;
      }
      for (W = r(g, W); !ee.done; V++, ee = y.next()) ee = L(W, g, V, ee.value, N), ee !== null && (e && ee.alternate !== null && W.delete(ee.key === null ? V : ee.key), h = i(ee, h, V), U === null ? A = ee : U.sibling = ee, U = ee);
      return e && W.forEach(function(ip) {
        return n(g, ip);
      }), ae && ct(g, V), A;
    }
    function ye(g, h, y, N) {
      if (typeof y == "object" && y !== null && y.type === Ee && y.key === null && (y = y.props.children), typeof y == "object" && y !== null) {
        switch (y.$$typeof) {
          case pe:
            e: {
              for (var A = y.key, U = h; U !== null; ) {
                if (U.key === A) {
                  if (A = y.type, A === Ee) {
                    if (U.tag === 7) {
                      t(g, U.sibling), h = o(U, y.props.children), h.return = g, g = h;
                      break e;
                    }
                  } else if (U.elementType === A || typeof A == "object" && A !== null && A.$$typeof === Ve && Ks(A) === U.type) {
                    t(g, U.sibling), h = o(U, y.props), h.ref = wr(g, U, y), h.return = g, g = h;
                    break e;
                  }
                  t(g, U);
                  break;
                } else n(g, U);
                U = U.sibling;
              }
              y.type === Ee ? (h = yt(y.props.children, g.mode, N, y.key), h.return = g, g = h) : (N = Wl(y.type, y.key, y.props, null, g.mode, N), N.ref = wr(g, h, y), N.return = g, g = N);
            }
            return a(g);
          case Ce:
            e: {
              for (U = y.key; h !== null; ) {
                if (h.key === U) if (h.tag === 4 && h.stateNode.containerInfo === y.containerInfo && h.stateNode.implementation === y.implementation) {
                  t(g, h.sibling), h = o(h, y.children || []), h.return = g, g = h;
                  break e;
                } else {
                  t(g, h);
                  break;
                }
                else n(g, h);
                h = h.sibling;
              }
              h = Ki(y, g.mode, N), h.return = g, g = h;
            }
            return a(g);
          case Ve:
            return U = y._init, ye(g, h, U(y._payload), N);
        }
        if (qt(y)) return I(g, h, y, N);
        if (H(y)) return F(g, h, y, N);
        vl(g, y);
      }
      return typeof y == "string" && y !== "" || typeof y == "number" ? (y = "" + y, h !== null && h.tag === 6 ? (t(g, h.sibling), h = o(h, y), h.return = g, g = h) : (t(g, h), h = Qi(y, g.mode, N), h.return = g, g = h), a(g)) : t(g, h);
    }
    return ye;
  }
  var Ut = Ys(!0), qs = Ys(!1), gl = Qn(null), yl = null, Wt = null, ni = null;
  function ti() {
    ni = Wt = yl = null;
  }
  function ri(e) {
    var n = gl.current;
    ie(gl), e._currentValue = n;
  }
  function li(e, n, t) {
    for (; e !== null; ) {
      var r = e.alternate;
      if ((e.childLanes & n) !== n ? (e.childLanes |= n, r !== null && (r.childLanes |= n)) : r !== null && (r.childLanes & n) !== n && (r.childLanes |= n), e === t) break;
      e = e.return;
    }
  }
  function Ht(e, n) {
    yl = e, ni = Wt = null, e = e.dependencies, e !== null && e.firstContext !== null && ((e.lanes & n) !== 0 && (Ke = !0), e.firstContext = null);
  }
  function un(e) {
    var n = e._currentValue;
    if (ni !== e) if (e = { context: e, memoizedValue: n, next: null }, Wt === null) {
      if (yl === null) throw Error(s(308));
      Wt = e, yl.dependencies = { lanes: 0, firstContext: e };
    } else Wt = Wt.next = e;
    return n;
  }
  var ft = null;
  function oi(e) {
    ft === null ? ft = [e] : ft.push(e);
  }
  function Xs(e, n, t, r) {
    var o = n.interleaved;
    return o === null ? (t.next = t, oi(n)) : (t.next = o.next, o.next = t), n.interleaved = t, Rn(e, r);
  }
  function Rn(e, n) {
    e.lanes |= n;
    var t = e.alternate;
    for (t !== null && (t.lanes |= n), t = e, e = e.return; e !== null; ) e.childLanes |= n, t = e.alternate, t !== null && (t.childLanes |= n), t = e, e = e.return;
    return t.tag === 3 ? t.stateNode : null;
  }
  var qn = !1;
  function ii(e) {
    e.updateQueue = { baseState: e.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
  }
  function Gs(e, n) {
    e = e.updateQueue, n.updateQueue === e && (n.updateQueue = { baseState: e.baseState, firstBaseUpdate: e.firstBaseUpdate, lastBaseUpdate: e.lastBaseUpdate, shared: e.shared, effects: e.effects });
  }
  function Dn(e, n) {
    return { eventTime: e, lane: n, tag: 0, payload: null, callback: null, next: null };
  }
  function Xn(e, n, t) {
    var r = e.updateQueue;
    if (r === null) return null;
    if (r = r.shared, (Z & 2) !== 0) {
      var o = r.pending;
      return o === null ? n.next = n : (n.next = o.next, o.next = n), r.pending = n, Rn(e, t);
    }
    return o = r.interleaved, o === null ? (n.next = n, oi(r)) : (n.next = o.next, o.next = n), r.interleaved = n, Rn(e, t);
  }
  function wl(e, n, t) {
    if (n = n.updateQueue, n !== null && (n = n.shared, (t & 4194240) !== 0)) {
      var r = n.lanes;
      r &= e.pendingLanes, t |= r, n.lanes = t, ko(e, t);
    }
  }
  function Zs(e, n) {
    var t = e.updateQueue, r = e.alternate;
    if (r !== null && (r = r.updateQueue, t === r)) {
      var o = null, i = null;
      if (t = t.firstBaseUpdate, t !== null) {
        do {
          var a = { eventTime: t.eventTime, lane: t.lane, tag: t.tag, payload: t.payload, callback: t.callback, next: null };
          i === null ? o = i = a : i = i.next = a, t = t.next;
        } while (t !== null);
        i === null ? o = i = n : i = i.next = n;
      } else o = i = n;
      t = { baseState: r.baseState, firstBaseUpdate: o, lastBaseUpdate: i, shared: r.shared, effects: r.effects }, e.updateQueue = t;
      return;
    }
    e = t.lastBaseUpdate, e === null ? t.firstBaseUpdate = n : e.next = n, t.lastBaseUpdate = n;
  }
  function kl(e, n, t, r) {
    var o = e.updateQueue;
    qn = !1;
    var i = o.firstBaseUpdate, a = o.lastBaseUpdate, d = o.shared.pending;
    if (d !== null) {
      o.shared.pending = null;
      var p = d, w = p.next;
      p.next = null, a === null ? i = w : a.next = w, a = p;
      var x = e.alternate;
      x !== null && (x = x.updateQueue, d = x.lastBaseUpdate, d !== a && (d === null ? x.firstBaseUpdate = w : d.next = w, x.lastBaseUpdate = p));
    }
    if (i !== null) {
      var P = o.baseState;
      a = 0, x = w = p = null, d = i;
      do {
        var C = d.lane, L = d.eventTime;
        if ((r & C) === C) {
          x !== null && (x = x.next = {
            eventTime: L,
            lane: 0,
            tag: d.tag,
            payload: d.payload,
            callback: d.callback,
            next: null
          });
          e: {
            var I = e, F = d;
            switch (C = n, L = t, F.tag) {
              case 1:
                if (I = F.payload, typeof I == "function") {
                  P = I.call(L, P, C);
                  break e;
                }
                P = I;
                break e;
              case 3:
                I.flags = I.flags & -65537 | 128;
              case 0:
                if (I = F.payload, C = typeof I == "function" ? I.call(L, P, C) : I, C == null) break e;
                P = D({}, P, C);
                break e;
              case 2:
                qn = !0;
            }
          }
          d.callback !== null && d.lane !== 0 && (e.flags |= 64, C = o.effects, C === null ? o.effects = [d] : C.push(d));
        } else L = { eventTime: L, lane: C, tag: d.tag, payload: d.payload, callback: d.callback, next: null }, x === null ? (w = x = L, p = P) : x = x.next = L, a |= C;
        if (d = d.next, d === null) {
          if (d = o.shared.pending, d === null) break;
          C = d, d = C.next, C.next = null, o.lastBaseUpdate = C, o.shared.pending = null;
        }
      } while (!0);
      if (x === null && (p = P), o.baseState = p, o.firstBaseUpdate = w, o.lastBaseUpdate = x, n = o.shared.interleaved, n !== null) {
        o = n;
        do
          a |= o.lane, o = o.next;
        while (o !== n);
      } else i === null && (o.shared.lanes = 0);
      ht |= a, e.lanes = a, e.memoizedState = P;
    }
  }
  function Js(e, n, t) {
    if (e = n.effects, n.effects = null, e !== null) for (n = 0; n < e.length; n++) {
      var r = e[n], o = r.callback;
      if (o !== null) {
        if (r.callback = null, r = t, typeof o != "function") throw Error(s(191, o));
        o.call(r);
      }
    }
  }
  var kr = {}, _n = Qn(kr), Sr = Qn(kr), Cr = Qn(kr);
  function dt(e) {
    if (e === kr) throw Error(s(174));
    return e;
  }
  function ui(e, n) {
    switch (le(Cr, n), le(Sr, e), le(_n, kr), e = n.nodeType, e) {
      case 9:
      case 11:
        n = (n = n.documentElement) ? n.namespaceURI : uo(null, "");
        break;
      default:
        e = e === 8 ? n.parentNode : n, n = e.namespaceURI || null, e = e.tagName, n = uo(n, e);
    }
    ie(_n), le(_n, n);
  }
  function Bt() {
    ie(_n), ie(Sr), ie(Cr);
  }
  function bs(e) {
    dt(Cr.current);
    var n = dt(_n.current), t = uo(n, e.type);
    n !== t && (le(Sr, e), le(_n, t));
  }
  function si(e) {
    Sr.current === e && (ie(_n), ie(Sr));
  }
  var ce = Qn(0);
  function Sl(e) {
    for (var n = e; n !== null; ) {
      if (n.tag === 13) {
        var t = n.memoizedState;
        if (t !== null && (t = t.dehydrated, t === null || t.data === "$?" || t.data === "$!")) return n;
      } else if (n.tag === 19 && n.memoizedProps.revealOrder !== void 0) {
        if ((n.flags & 128) !== 0) return n;
      } else if (n.child !== null) {
        n.child.return = n, n = n.child;
        continue;
      }
      if (n === e) break;
      for (; n.sibling === null; ) {
        if (n.return === null || n.return === e) return null;
        n = n.return;
      }
      n.sibling.return = n.return, n = n.sibling;
    }
    return null;
  }
  var ai = [];
  function ci() {
    for (var e = 0; e < ai.length; e++) ai[e]._workInProgressVersionPrimary = null;
    ai.length = 0;
  }
  var Cl = we.ReactCurrentDispatcher, fi = we.ReactCurrentBatchConfig, pt = 0, fe = null, _e = null, ze = null, El = !1, Er = !1, _r = 0, zd = 0;
  function Ie() {
    throw Error(s(321));
  }
  function di(e, n) {
    if (n === null) return !1;
    for (var t = 0; t < n.length && t < e.length; t++) if (!mn(e[t], n[t])) return !1;
    return !0;
  }
  function pi(e, n, t, r, o, i) {
    if (pt = i, fe = n, n.memoizedState = null, n.updateQueue = null, n.lanes = 0, Cl.current = e === null || e.memoizedState === null ? Rd : Dd, e = t(r, o), Er) {
      i = 0;
      do {
        if (Er = !1, _r = 0, 25 <= i) throw Error(s(301));
        i += 1, ze = _e = null, n.updateQueue = null, Cl.current = Od, e = t(r, o);
      } while (Er);
    }
    if (Cl.current = Pl, n = _e !== null && _e.next !== null, pt = 0, ze = _e = fe = null, El = !1, n) throw Error(s(300));
    return e;
  }
  function hi() {
    var e = _r !== 0;
    return _r = 0, e;
  }
  function xn() {
    var e = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
    return ze === null ? fe.memoizedState = ze = e : ze = ze.next = e, ze;
  }
  function sn() {
    if (_e === null) {
      var e = fe.alternate;
      e = e !== null ? e.memoizedState : null;
    } else e = _e.next;
    var n = ze === null ? fe.memoizedState : ze.next;
    if (n !== null) ze = n, _e = e;
    else {
      if (e === null) throw Error(s(310));
      _e = e, e = { memoizedState: _e.memoizedState, baseState: _e.baseState, baseQueue: _e.baseQueue, queue: _e.queue, next: null }, ze === null ? fe.memoizedState = ze = e : ze = ze.next = e;
    }
    return ze;
  }
  function xr(e, n) {
    return typeof n == "function" ? n(e) : n;
  }
  function mi(e) {
    var n = sn(), t = n.queue;
    if (t === null) throw Error(s(311));
    t.lastRenderedReducer = e;
    var r = _e, o = r.baseQueue, i = t.pending;
    if (i !== null) {
      if (o !== null) {
        var a = o.next;
        o.next = i.next, i.next = a;
      }
      r.baseQueue = o = i, t.pending = null;
    }
    if (o !== null) {
      i = o.next, r = r.baseState;
      var d = a = null, p = null, w = i;
      do {
        var x = w.lane;
        if ((pt & x) === x) p !== null && (p = p.next = { lane: 0, action: w.action, hasEagerState: w.hasEagerState, eagerState: w.eagerState, next: null }), r = w.hasEagerState ? w.eagerState : e(r, w.action);
        else {
          var P = {
            lane: x,
            action: w.action,
            hasEagerState: w.hasEagerState,
            eagerState: w.eagerState,
            next: null
          };
          p === null ? (d = p = P, a = r) : p = p.next = P, fe.lanes |= x, ht |= x;
        }
        w = w.next;
      } while (w !== null && w !== i);
      p === null ? a = r : p.next = d, mn(r, n.memoizedState) || (Ke = !0), n.memoizedState = r, n.baseState = a, n.baseQueue = p, t.lastRenderedState = r;
    }
    if (e = t.interleaved, e !== null) {
      o = e;
      do
        i = o.lane, fe.lanes |= i, ht |= i, o = o.next;
      while (o !== e);
    } else o === null && (t.lanes = 0);
    return [n.memoizedState, t.dispatch];
  }
  function vi(e) {
    var n = sn(), t = n.queue;
    if (t === null) throw Error(s(311));
    t.lastRenderedReducer = e;
    var r = t.dispatch, o = t.pending, i = n.memoizedState;
    if (o !== null) {
      t.pending = null;
      var a = o = o.next;
      do
        i = e(i, a.action), a = a.next;
      while (a !== o);
      mn(i, n.memoizedState) || (Ke = !0), n.memoizedState = i, n.baseQueue === null && (n.baseState = i), t.lastRenderedState = i;
    }
    return [i, r];
  }
  function ea() {
  }
  function na(e, n) {
    var t = fe, r = sn(), o = n(), i = !mn(r.memoizedState, o);
    if (i && (r.memoizedState = o, Ke = !0), r = r.queue, gi(la.bind(null, t, r, e), [e]), r.getSnapshot !== n || i || ze !== null && ze.memoizedState.tag & 1) {
      if (t.flags |= 2048, Pr(9, ra.bind(null, t, r, o, n), void 0, null), Me === null) throw Error(s(349));
      (pt & 30) !== 0 || ta(t, n, o);
    }
    return o;
  }
  function ta(e, n, t) {
    e.flags |= 16384, e = { getSnapshot: n, value: t }, n = fe.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, fe.updateQueue = n, n.stores = [e]) : (t = n.stores, t === null ? n.stores = [e] : t.push(e));
  }
  function ra(e, n, t, r) {
    n.value = t, n.getSnapshot = r, oa(n) && ia(e);
  }
  function la(e, n, t) {
    return t(function() {
      oa(n) && ia(e);
    });
  }
  function oa(e) {
    var n = e.getSnapshot;
    e = e.value;
    try {
      var t = n();
      return !mn(e, t);
    } catch {
      return !0;
    }
  }
  function ia(e) {
    var n = Rn(e, 1);
    n !== null && kn(n, e, 1, -1);
  }
  function ua(e) {
    var n = xn();
    return typeof e == "function" && (e = e()), n.memoizedState = n.baseState = e, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: xr, lastRenderedState: e }, n.queue = e, e = e.dispatch = Ld.bind(null, fe, e), [n.memoizedState, e];
  }
  function Pr(e, n, t, r) {
    return e = { tag: e, create: n, destroy: t, deps: r, next: null }, n = fe.updateQueue, n === null ? (n = { lastEffect: null, stores: null }, fe.updateQueue = n, n.lastEffect = e.next = e) : (t = n.lastEffect, t === null ? n.lastEffect = e.next = e : (r = t.next, t.next = e, e.next = r, n.lastEffect = e)), e;
  }
  function sa() {
    return sn().memoizedState;
  }
  function _l(e, n, t, r) {
    var o = xn();
    fe.flags |= e, o.memoizedState = Pr(1 | n, t, void 0, r === void 0 ? null : r);
  }
  function xl(e, n, t, r) {
    var o = sn();
    r = r === void 0 ? null : r;
    var i = void 0;
    if (_e !== null) {
      var a = _e.memoizedState;
      if (i = a.destroy, r !== null && di(r, a.deps)) {
        o.memoizedState = Pr(n, t, i, r);
        return;
      }
    }
    fe.flags |= e, o.memoizedState = Pr(1 | n, t, i, r);
  }
  function aa(e, n) {
    return _l(8390656, 8, e, n);
  }
  function gi(e, n) {
    return xl(2048, 8, e, n);
  }
  function ca(e, n) {
    return xl(4, 2, e, n);
  }
  function fa(e, n) {
    return xl(4, 4, e, n);
  }
  function da(e, n) {
    if (typeof n == "function") return e = e(), n(e), function() {
      n(null);
    };
    if (n != null) return e = e(), n.current = e, function() {
      n.current = null;
    };
  }
  function pa(e, n, t) {
    return t = t != null ? t.concat([e]) : null, xl(4, 4, da.bind(null, n, e), t);
  }
  function yi() {
  }
  function ha(e, n) {
    var t = sn();
    n = n === void 0 ? null : n;
    var r = t.memoizedState;
    return r !== null && n !== null && di(n, r[1]) ? r[0] : (t.memoizedState = [e, n], e);
  }
  function ma(e, n) {
    var t = sn();
    n = n === void 0 ? null : n;
    var r = t.memoizedState;
    return r !== null && n !== null && di(n, r[1]) ? r[0] : (e = e(), t.memoizedState = [e, n], e);
  }
  function va(e, n, t) {
    return (pt & 21) === 0 ? (e.baseState && (e.baseState = !1, Ke = !0), e.memoizedState = t) : (mn(t, n) || (t = Ku(), fe.lanes |= t, ht |= t, e.baseState = !0), n);
  }
  function Md(e, n) {
    var t = te;
    te = t !== 0 && 4 > t ? t : 4, e(!0);
    var r = fi.transition;
    fi.transition = {};
    try {
      e(!1), n();
    } finally {
      te = t, fi.transition = r;
    }
  }
  function ga() {
    return sn().memoizedState;
  }
  function Td(e, n, t) {
    var r = bn(e);
    if (t = { lane: r, action: t, hasEagerState: !1, eagerState: null, next: null }, ya(e)) wa(n, t);
    else if (t = Xs(e, n, t, r), t !== null) {
      var o = We();
      kn(t, e, r, o), ka(t, n, r);
    }
  }
  function Ld(e, n, t) {
    var r = bn(e), o = { lane: r, action: t, hasEagerState: !1, eagerState: null, next: null };
    if (ya(e)) wa(n, o);
    else {
      var i = e.alternate;
      if (e.lanes === 0 && (i === null || i.lanes === 0) && (i = n.lastRenderedReducer, i !== null)) try {
        var a = n.lastRenderedState, d = i(a, t);
        if (o.hasEagerState = !0, o.eagerState = d, mn(d, a)) {
          var p = n.interleaved;
          p === null ? (o.next = o, oi(n)) : (o.next = p.next, p.next = o), n.interleaved = o;
          return;
        }
      } catch {
      }
      t = Xs(e, n, o, r), t !== null && (o = We(), kn(t, e, r, o), ka(t, n, r));
    }
  }
  function ya(e) {
    var n = e.alternate;
    return e === fe || n !== null && n === fe;
  }
  function wa(e, n) {
    Er = El = !0;
    var t = e.pending;
    t === null ? n.next = n : (n.next = t.next, t.next = n), e.pending = n;
  }
  function ka(e, n, t) {
    if ((t & 4194240) !== 0) {
      var r = n.lanes;
      r &= e.pendingLanes, t |= r, n.lanes = t, ko(e, t);
    }
  }
  var Pl = { readContext: un, useCallback: Ie, useContext: Ie, useEffect: Ie, useImperativeHandle: Ie, useInsertionEffect: Ie, useLayoutEffect: Ie, useMemo: Ie, useReducer: Ie, useRef: Ie, useState: Ie, useDebugValue: Ie, useDeferredValue: Ie, useTransition: Ie, useMutableSource: Ie, useSyncExternalStore: Ie, useId: Ie, unstable_isNewReconciler: !1 }, Rd = { readContext: un, useCallback: function(e, n) {
    return xn().memoizedState = [e, n === void 0 ? null : n], e;
  }, useContext: un, useEffect: aa, useImperativeHandle: function(e, n, t) {
    return t = t != null ? t.concat([e]) : null, _l(
      4194308,
      4,
      da.bind(null, n, e),
      t
    );
  }, useLayoutEffect: function(e, n) {
    return _l(4194308, 4, e, n);
  }, useInsertionEffect: function(e, n) {
    return _l(4, 2, e, n);
  }, useMemo: function(e, n) {
    var t = xn();
    return n = n === void 0 ? null : n, e = e(), t.memoizedState = [e, n], e;
  }, useReducer: function(e, n, t) {
    var r = xn();
    return n = t !== void 0 ? t(n) : n, r.memoizedState = r.baseState = n, e = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: e, lastRenderedState: n }, r.queue = e, e = e.dispatch = Td.bind(null, fe, e), [r.memoizedState, e];
  }, useRef: function(e) {
    var n = xn();
    return e = { current: e }, n.memoizedState = e;
  }, useState: ua, useDebugValue: yi, useDeferredValue: function(e) {
    return xn().memoizedState = e;
  }, useTransition: function() {
    var e = ua(!1), n = e[0];
    return e = Md.bind(null, e[1]), xn().memoizedState = e, [n, e];
  }, useMutableSource: function() {
  }, useSyncExternalStore: function(e, n, t) {
    var r = fe, o = xn();
    if (ae) {
      if (t === void 0) throw Error(s(407));
      t = t();
    } else {
      if (t = n(), Me === null) throw Error(s(349));
      (pt & 30) !== 0 || ta(r, n, t);
    }
    o.memoizedState = t;
    var i = { value: t, getSnapshot: n };
    return o.queue = i, aa(la.bind(
      null,
      r,
      i,
      e
    ), [e]), r.flags |= 2048, Pr(9, ra.bind(null, r, i, t, n), void 0, null), t;
  }, useId: function() {
    var e = xn(), n = Me.identifierPrefix;
    if (ae) {
      var t = Ln, r = Tn;
      t = (r & ~(1 << 32 - hn(r) - 1)).toString(32) + t, n = ":" + n + "R" + t, t = _r++, 0 < t && (n += "H" + t.toString(32)), n += ":";
    } else t = zd++, n = ":" + n + "r" + t.toString(32) + ":";
    return e.memoizedState = n;
  }, unstable_isNewReconciler: !1 }, Dd = {
    readContext: un,
    useCallback: ha,
    useContext: un,
    useEffect: gi,
    useImperativeHandle: pa,
    useInsertionEffect: ca,
    useLayoutEffect: fa,
    useMemo: ma,
    useReducer: mi,
    useRef: sa,
    useState: function() {
      return mi(xr);
    },
    useDebugValue: yi,
    useDeferredValue: function(e) {
      var n = sn();
      return va(n, _e.memoizedState, e);
    },
    useTransition: function() {
      var e = mi(xr)[0], n = sn().memoizedState;
      return [e, n];
    },
    useMutableSource: ea,
    useSyncExternalStore: na,
    useId: ga,
    unstable_isNewReconciler: !1
  }, Od = { readContext: un, useCallback: ha, useContext: un, useEffect: gi, useImperativeHandle: pa, useInsertionEffect: ca, useLayoutEffect: fa, useMemo: ma, useReducer: vi, useRef: sa, useState: function() {
    return vi(xr);
  }, useDebugValue: yi, useDeferredValue: function(e) {
    var n = sn();
    return _e === null ? n.memoizedState = e : va(n, _e.memoizedState, e);
  }, useTransition: function() {
    var e = vi(xr)[0], n = sn().memoizedState;
    return [e, n];
  }, useMutableSource: ea, useSyncExternalStore: na, useId: ga, unstable_isNewReconciler: !1 };
  function gn(e, n) {
    if (e && e.defaultProps) {
      n = D({}, n), e = e.defaultProps;
      for (var t in e) n[t] === void 0 && (n[t] = e[t]);
      return n;
    }
    return n;
  }
  function wi(e, n, t, r) {
    n = e.memoizedState, t = t(r, n), t = t == null ? n : D({}, n, t), e.memoizedState = t, e.lanes === 0 && (e.updateQueue.baseState = t);
  }
  var Nl = { isMounted: function(e) {
    return (e = e._reactInternals) ? it(e) === e : !1;
  }, enqueueSetState: function(e, n, t) {
    e = e._reactInternals;
    var r = We(), o = bn(e), i = Dn(r, o);
    i.payload = n, t != null && (i.callback = t), n = Xn(e, i, o), n !== null && (kn(n, e, o, r), wl(n, e, o));
  }, enqueueReplaceState: function(e, n, t) {
    e = e._reactInternals;
    var r = We(), o = bn(e), i = Dn(r, o);
    i.tag = 1, i.payload = n, t != null && (i.callback = t), n = Xn(e, i, o), n !== null && (kn(n, e, o, r), wl(n, e, o));
  }, enqueueForceUpdate: function(e, n) {
    e = e._reactInternals;
    var t = We(), r = bn(e), o = Dn(t, r);
    o.tag = 2, n != null && (o.callback = n), n = Xn(e, o, r), n !== null && (kn(n, e, r, t), wl(n, e, r));
  } };
  function Sa(e, n, t, r, o, i, a) {
    return e = e.stateNode, typeof e.shouldComponentUpdate == "function" ? e.shouldComponentUpdate(r, i, a) : n.prototype && n.prototype.isPureReactComponent ? !dr(t, r) || !dr(o, i) : !0;
  }
  function Ca(e, n, t) {
    var r = !1, o = Kn, i = n.contextType;
    return typeof i == "object" && i !== null ? i = un(i) : (o = Qe(n) ? st : Oe.current, r = n.contextTypes, i = (r = r != null) ? It(e, o) : Kn), n = new n(t, i), e.memoizedState = n.state !== null && n.state !== void 0 ? n.state : null, n.updater = Nl, e.stateNode = n, n._reactInternals = e, r && (e = e.stateNode, e.__reactInternalMemoizedUnmaskedChildContext = o, e.__reactInternalMemoizedMaskedChildContext = i), n;
  }
  function Ea(e, n, t, r) {
    e = n.state, typeof n.componentWillReceiveProps == "function" && n.componentWillReceiveProps(t, r), typeof n.UNSAFE_componentWillReceiveProps == "function" && n.UNSAFE_componentWillReceiveProps(t, r), n.state !== e && Nl.enqueueReplaceState(n, n.state, null);
  }
  function ki(e, n, t, r) {
    var o = e.stateNode;
    o.props = t, o.state = e.memoizedState, o.refs = {}, ii(e);
    var i = n.contextType;
    typeof i == "object" && i !== null ? o.context = un(i) : (i = Qe(n) ? st : Oe.current, o.context = It(e, i)), o.state = e.memoizedState, i = n.getDerivedStateFromProps, typeof i == "function" && (wi(e, n, i, t), o.state = e.memoizedState), typeof n.getDerivedStateFromProps == "function" || typeof o.getSnapshotBeforeUpdate == "function" || typeof o.UNSAFE_componentWillMount != "function" && typeof o.componentWillMount != "function" || (n = o.state, typeof o.componentWillMount == "function" && o.componentWillMount(), typeof o.UNSAFE_componentWillMount == "function" && o.UNSAFE_componentWillMount(), n !== o.state && Nl.enqueueReplaceState(o, o.state, null), kl(e, t, o, r), o.state = e.memoizedState), typeof o.componentDidMount == "function" && (e.flags |= 4194308);
  }
  function Vt(e, n) {
    try {
      var t = "", r = n;
      do
        t += J(r), r = r.return;
      while (r);
      var o = t;
    } catch (i) {
      o = `
Error generating stack: ` + i.message + `
` + i.stack;
    }
    return { value: e, source: n, stack: o, digest: null };
  }
  function Si(e, n, t) {
    return { value: e, source: null, stack: t ?? null, digest: n ?? null };
  }
  function Ci(e, n) {
    try {
      console.error(n.value);
    } catch (t) {
      setTimeout(function() {
        throw t;
      });
    }
  }
  var Id = typeof WeakMap == "function" ? WeakMap : Map;
  function _a(e, n, t) {
    t = Dn(-1, t), t.tag = 3, t.payload = { element: null };
    var r = n.value;
    return t.callback = function() {
      Ol || (Ol = !0, ji = r), Ci(e, n);
    }, t;
  }
  function xa(e, n, t) {
    t = Dn(-1, t), t.tag = 3;
    var r = e.type.getDerivedStateFromError;
    if (typeof r == "function") {
      var o = n.value;
      t.payload = function() {
        return r(o);
      }, t.callback = function() {
        Ci(e, n);
      };
    }
    var i = e.stateNode;
    return i !== null && typeof i.componentDidCatch == "function" && (t.callback = function() {
      Ci(e, n), typeof r != "function" && (Zn === null ? Zn = /* @__PURE__ */ new Set([this]) : Zn.add(this));
      var a = n.stack;
      this.componentDidCatch(n.value, { componentStack: a !== null ? a : "" });
    }), t;
  }
  function Pa(e, n, t) {
    var r = e.pingCache;
    if (r === null) {
      r = e.pingCache = new Id();
      var o = /* @__PURE__ */ new Set();
      r.set(n, o);
    } else o = r.get(n), o === void 0 && (o = /* @__PURE__ */ new Set(), r.set(n, o));
    o.has(t) || (o.add(t), e = Xd.bind(null, e, n, t), n.then(e, e));
  }
  function Na(e) {
    do {
      var n;
      if ((n = e.tag === 13) && (n = e.memoizedState, n = n !== null ? n.dehydrated !== null : !0), n) return e;
      e = e.return;
    } while (e !== null);
    return null;
  }
  function za(e, n, t, r, o) {
    return (e.mode & 1) === 0 ? (e === n ? e.flags |= 65536 : (e.flags |= 128, t.flags |= 131072, t.flags &= -52805, t.tag === 1 && (t.alternate === null ? t.tag = 17 : (n = Dn(-1, 1), n.tag = 2, Xn(t, n, 1))), t.lanes |= 1), e) : (e.flags |= 65536, e.lanes = o, e);
  }
  var Fd = we.ReactCurrentOwner, Ke = !1;
  function Ue(e, n, t, r) {
    n.child = e === null ? qs(n, null, t, r) : Ut(n, e.child, t, r);
  }
  function Ma(e, n, t, r, o) {
    t = t.render;
    var i = n.ref;
    return Ht(n, o), r = pi(e, n, t, r, i, o), t = hi(), e !== null && !Ke ? (n.updateQueue = e.updateQueue, n.flags &= -2053, e.lanes &= ~o, On(e, n, o)) : (ae && t && Go(n), n.flags |= 1, Ue(e, n, r, o), n.child);
  }
  function Ta(e, n, t, r, o) {
    if (e === null) {
      var i = t.type;
      return typeof i == "function" && !$i(i) && i.defaultProps === void 0 && t.compare === null && t.defaultProps === void 0 ? (n.tag = 15, n.type = i, La(e, n, i, r, o)) : (e = Wl(t.type, null, r, n, n.mode, o), e.ref = n.ref, e.return = n, n.child = e);
    }
    if (i = e.child, (e.lanes & o) === 0) {
      var a = i.memoizedProps;
      if (t = t.compare, t = t !== null ? t : dr, t(a, r) && e.ref === n.ref) return On(e, n, o);
    }
    return n.flags |= 1, e = nt(i, r), e.ref = n.ref, e.return = n, n.child = e;
  }
  function La(e, n, t, r, o) {
    if (e !== null) {
      var i = e.memoizedProps;
      if (dr(i, r) && e.ref === n.ref) if (Ke = !1, n.pendingProps = r = i, (e.lanes & o) !== 0) (e.flags & 131072) !== 0 && (Ke = !0);
      else return n.lanes = e.lanes, On(e, n, o);
    }
    return Ei(e, n, t, r, o);
  }
  function Ra(e, n, t) {
    var r = n.pendingProps, o = r.children, i = e !== null ? e.memoizedState : null;
    if (r.mode === "hidden") if ((n.mode & 1) === 0) n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, le(Qt, rn), rn |= t;
    else {
      if ((t & 1073741824) === 0) return e = i !== null ? i.baseLanes | t : t, n.lanes = n.childLanes = 1073741824, n.memoizedState = { baseLanes: e, cachePool: null, transitions: null }, n.updateQueue = null, le(Qt, rn), rn |= e, null;
      n.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, r = i !== null ? i.baseLanes : t, le(Qt, rn), rn |= r;
    }
    else i !== null ? (r = i.baseLanes | t, n.memoizedState = null) : r = t, le(Qt, rn), rn |= r;
    return Ue(e, n, o, t), n.child;
  }
  function Da(e, n) {
    var t = n.ref;
    (e === null && t !== null || e !== null && e.ref !== t) && (n.flags |= 512, n.flags |= 2097152);
  }
  function Ei(e, n, t, r, o) {
    var i = Qe(t) ? st : Oe.current;
    return i = It(n, i), Ht(n, o), t = pi(e, n, t, r, i, o), r = hi(), e !== null && !Ke ? (n.updateQueue = e.updateQueue, n.flags &= -2053, e.lanes &= ~o, On(e, n, o)) : (ae && r && Go(n), n.flags |= 1, Ue(e, n, t, o), n.child);
  }
  function Oa(e, n, t, r, o) {
    if (Qe(t)) {
      var i = !0;
      fl(n);
    } else i = !1;
    if (Ht(n, o), n.stateNode === null) Ml(e, n), Ca(n, t, r), ki(n, t, r, o), r = !0;
    else if (e === null) {
      var a = n.stateNode, d = n.memoizedProps;
      a.props = d;
      var p = a.context, w = t.contextType;
      typeof w == "object" && w !== null ? w = un(w) : (w = Qe(t) ? st : Oe.current, w = It(n, w));
      var x = t.getDerivedStateFromProps, P = typeof x == "function" || typeof a.getSnapshotBeforeUpdate == "function";
      P || typeof a.UNSAFE_componentWillReceiveProps != "function" && typeof a.componentWillReceiveProps != "function" || (d !== r || p !== w) && Ea(n, a, r, w), qn = !1;
      var C = n.memoizedState;
      a.state = C, kl(n, r, a, o), p = n.memoizedState, d !== r || C !== p || $e.current || qn ? (typeof x == "function" && (wi(n, t, x, r), p = n.memoizedState), (d = qn || Sa(n, t, d, r, C, p, w)) ? (P || typeof a.UNSAFE_componentWillMount != "function" && typeof a.componentWillMount != "function" || (typeof a.componentWillMount == "function" && a.componentWillMount(), typeof a.UNSAFE_componentWillMount == "function" && a.UNSAFE_componentWillMount()), typeof a.componentDidMount == "function" && (n.flags |= 4194308)) : (typeof a.componentDidMount == "function" && (n.flags |= 4194308), n.memoizedProps = r, n.memoizedState = p), a.props = r, a.state = p, a.context = w, r = d) : (typeof a.componentDidMount == "function" && (n.flags |= 4194308), r = !1);
    } else {
      a = n.stateNode, Gs(e, n), d = n.memoizedProps, w = n.type === n.elementType ? d : gn(n.type, d), a.props = w, P = n.pendingProps, C = a.context, p = t.contextType, typeof p == "object" && p !== null ? p = un(p) : (p = Qe(t) ? st : Oe.current, p = It(n, p));
      var L = t.getDerivedStateFromProps;
      (x = typeof L == "function" || typeof a.getSnapshotBeforeUpdate == "function") || typeof a.UNSAFE_componentWillReceiveProps != "function" && typeof a.componentWillReceiveProps != "function" || (d !== P || C !== p) && Ea(n, a, r, p), qn = !1, C = n.memoizedState, a.state = C, kl(n, r, a, o);
      var I = n.memoizedState;
      d !== P || C !== I || $e.current || qn ? (typeof L == "function" && (wi(n, t, L, r), I = n.memoizedState), (w = qn || Sa(n, t, w, r, C, I, p) || !1) ? (x || typeof a.UNSAFE_componentWillUpdate != "function" && typeof a.componentWillUpdate != "function" || (typeof a.componentWillUpdate == "function" && a.componentWillUpdate(r, I, p), typeof a.UNSAFE_componentWillUpdate == "function" && a.UNSAFE_componentWillUpdate(r, I, p)), typeof a.componentDidUpdate == "function" && (n.flags |= 4), typeof a.getSnapshotBeforeUpdate == "function" && (n.flags |= 1024)) : (typeof a.componentDidUpdate != "function" || d === e.memoizedProps && C === e.memoizedState || (n.flags |= 4), typeof a.getSnapshotBeforeUpdate != "function" || d === e.memoizedProps && C === e.memoizedState || (n.flags |= 1024), n.memoizedProps = r, n.memoizedState = I), a.props = r, a.state = I, a.context = p, r = w) : (typeof a.componentDidUpdate != "function" || d === e.memoizedProps && C === e.memoizedState || (n.flags |= 4), typeof a.getSnapshotBeforeUpdate != "function" || d === e.memoizedProps && C === e.memoizedState || (n.flags |= 1024), r = !1);
    }
    return _i(e, n, t, r, i, o);
  }
  function _i(e, n, t, r, o, i) {
    Da(e, n);
    var a = (n.flags & 128) !== 0;
    if (!r && !a) return o && Us(n, t, !1), On(e, n, i);
    r = n.stateNode, Fd.current = n;
    var d = a && typeof t.getDerivedStateFromError != "function" ? null : r.render();
    return n.flags |= 1, e !== null && a ? (n.child = Ut(n, e.child, null, i), n.child = Ut(n, null, d, i)) : Ue(e, n, d, i), n.memoizedState = r.state, o && Us(n, t, !0), n.child;
  }
  function Ia(e) {
    var n = e.stateNode;
    n.pendingContext ? js(e, n.pendingContext, n.pendingContext !== n.context) : n.context && js(e, n.context, !1), ui(e, n.containerInfo);
  }
  function Fa(e, n, t, r, o) {
    return At(), ei(o), n.flags |= 256, Ue(e, n, t, r), n.child;
  }
  var xi = { dehydrated: null, treeContext: null, retryLane: 0 };
  function Pi(e) {
    return { baseLanes: e, cachePool: null, transitions: null };
  }
  function ja(e, n, t) {
    var r = n.pendingProps, o = ce.current, i = !1, a = (n.flags & 128) !== 0, d;
    if ((d = a) || (d = e !== null && e.memoizedState === null ? !1 : (o & 2) !== 0), d ? (i = !0, n.flags &= -129) : (e === null || e.memoizedState !== null) && (o |= 1), le(ce, o & 1), e === null)
      return bo(n), e = n.memoizedState, e !== null && (e = e.dehydrated, e !== null) ? ((n.mode & 1) === 0 ? n.lanes = 1 : e.data === "$!" ? n.lanes = 8 : n.lanes = 1073741824, null) : (a = r.children, e = r.fallback, i ? (r = n.mode, i = n.child, a = { mode: "hidden", children: a }, (r & 1) === 0 && i !== null ? (i.childLanes = 0, i.pendingProps = a) : i = Hl(a, r, 0, null), e = yt(e, r, t, null), i.return = n, e.return = n, i.sibling = e, n.child = i, n.child.memoizedState = Pi(t), n.memoizedState = xi, e) : Ni(n, a));
    if (o = e.memoizedState, o !== null && (d = o.dehydrated, d !== null)) return jd(e, n, a, r, d, o, t);
    if (i) {
      i = r.fallback, a = n.mode, o = e.child, d = o.sibling;
      var p = { mode: "hidden", children: r.children };
      return (a & 1) === 0 && n.child !== o ? (r = n.child, r.childLanes = 0, r.pendingProps = p, n.deletions = null) : (r = nt(o, p), r.subtreeFlags = o.subtreeFlags & 14680064), d !== null ? i = nt(d, i) : (i = yt(i, a, t, null), i.flags |= 2), i.return = n, r.return = n, r.sibling = i, n.child = r, r = i, i = n.child, a = e.child.memoizedState, a = a === null ? Pi(t) : { baseLanes: a.baseLanes | t, cachePool: null, transitions: a.transitions }, i.memoizedState = a, i.childLanes = e.childLanes & ~t, n.memoizedState = xi, r;
    }
    return i = e.child, e = i.sibling, r = nt(i, { mode: "visible", children: r.children }), (n.mode & 1) === 0 && (r.lanes = t), r.return = n, r.sibling = null, e !== null && (t = n.deletions, t === null ? (n.deletions = [e], n.flags |= 16) : t.push(e)), n.child = r, n.memoizedState = null, r;
  }
  function Ni(e, n) {
    return n = Hl({ mode: "visible", children: n }, e.mode, 0, null), n.return = e, e.child = n;
  }
  function zl(e, n, t, r) {
    return r !== null && ei(r), Ut(n, e.child, null, t), e = Ni(n, n.pendingProps.children), e.flags |= 2, n.memoizedState = null, e;
  }
  function jd(e, n, t, r, o, i, a) {
    if (t)
      return n.flags & 256 ? (n.flags &= -257, r = Si(Error(s(422))), zl(e, n, a, r)) : n.memoizedState !== null ? (n.child = e.child, n.flags |= 128, null) : (i = r.fallback, o = n.mode, r = Hl({ mode: "visible", children: r.children }, o, 0, null), i = yt(i, o, a, null), i.flags |= 2, r.return = n, i.return = n, r.sibling = i, n.child = r, (n.mode & 1) !== 0 && Ut(n, e.child, null, a), n.child.memoizedState = Pi(a), n.memoizedState = xi, i);
    if ((n.mode & 1) === 0) return zl(e, n, a, null);
    if (o.data === "$!") {
      if (r = o.nextSibling && o.nextSibling.dataset, r) var d = r.dgst;
      return r = d, i = Error(s(419)), r = Si(i, r, void 0), zl(e, n, a, r);
    }
    if (d = (a & e.childLanes) !== 0, Ke || d) {
      if (r = Me, r !== null) {
        switch (a & -a) {
          case 4:
            o = 2;
            break;
          case 16:
            o = 8;
            break;
          case 64:
          case 128:
          case 256:
          case 512:
          case 1024:
          case 2048:
          case 4096:
          case 8192:
          case 16384:
          case 32768:
          case 65536:
          case 131072:
          case 262144:
          case 524288:
          case 1048576:
          case 2097152:
          case 4194304:
          case 8388608:
          case 16777216:
          case 33554432:
          case 67108864:
            o = 32;
            break;
          case 536870912:
            o = 268435456;
            break;
          default:
            o = 0;
        }
        o = (o & (r.suspendedLanes | a)) !== 0 ? 0 : o, o !== 0 && o !== i.retryLane && (i.retryLane = o, Rn(e, o), kn(r, e, o, -1));
      }
      return Vi(), r = Si(Error(s(421))), zl(e, n, a, r);
    }
    return o.data === "$?" ? (n.flags |= 128, n.child = e.child, n = Gd.bind(null, e), o._reactRetry = n, null) : (e = i.treeContext, tn = $n(o.nextSibling), nn = n, ae = !0, vn = null, e !== null && (ln[on++] = Tn, ln[on++] = Ln, ln[on++] = at, Tn = e.id, Ln = e.overflow, at = n), n = Ni(n, r.children), n.flags |= 4096, n);
  }
  function Aa(e, n, t) {
    e.lanes |= n;
    var r = e.alternate;
    r !== null && (r.lanes |= n), li(e.return, n, t);
  }
  function zi(e, n, t, r, o) {
    var i = e.memoizedState;
    i === null ? e.memoizedState = { isBackwards: n, rendering: null, renderingStartTime: 0, last: r, tail: t, tailMode: o } : (i.isBackwards = n, i.rendering = null, i.renderingStartTime = 0, i.last = r, i.tail = t, i.tailMode = o);
  }
  function Ua(e, n, t) {
    var r = n.pendingProps, o = r.revealOrder, i = r.tail;
    if (Ue(e, n, r.children, t), r = ce.current, (r & 2) !== 0) r = r & 1 | 2, n.flags |= 128;
    else {
      if (e !== null && (e.flags & 128) !== 0) e: for (e = n.child; e !== null; ) {
        if (e.tag === 13) e.memoizedState !== null && Aa(e, t, n);
        else if (e.tag === 19) Aa(e, t, n);
        else if (e.child !== null) {
          e.child.return = e, e = e.child;
          continue;
        }
        if (e === n) break e;
        for (; e.sibling === null; ) {
          if (e.return === null || e.return === n) break e;
          e = e.return;
        }
        e.sibling.return = e.return, e = e.sibling;
      }
      r &= 1;
    }
    if (le(ce, r), (n.mode & 1) === 0) n.memoizedState = null;
    else switch (o) {
      case "forwards":
        for (t = n.child, o = null; t !== null; ) e = t.alternate, e !== null && Sl(e) === null && (o = t), t = t.sibling;
        t = o, t === null ? (o = n.child, n.child = null) : (o = t.sibling, t.sibling = null), zi(n, !1, o, t, i);
        break;
      case "backwards":
        for (t = null, o = n.child, n.child = null; o !== null; ) {
          if (e = o.alternate, e !== null && Sl(e) === null) {
            n.child = o;
            break;
          }
          e = o.sibling, o.sibling = t, t = o, o = e;
        }
        zi(n, !0, t, null, i);
        break;
      case "together":
        zi(n, !1, null, null, void 0);
        break;
      default:
        n.memoizedState = null;
    }
    return n.child;
  }
  function Ml(e, n) {
    (n.mode & 1) === 0 && e !== null && (e.alternate = null, n.alternate = null, n.flags |= 2);
  }
  function On(e, n, t) {
    if (e !== null && (n.dependencies = e.dependencies), ht |= n.lanes, (t & n.childLanes) === 0) return null;
    if (e !== null && n.child !== e.child) throw Error(s(153));
    if (n.child !== null) {
      for (e = n.child, t = nt(e, e.pendingProps), n.child = t, t.return = n; e.sibling !== null; ) e = e.sibling, t = t.sibling = nt(e, e.pendingProps), t.return = n;
      t.sibling = null;
    }
    return n.child;
  }
  function Ad(e, n, t) {
    switch (n.tag) {
      case 3:
        Ia(n), At();
        break;
      case 5:
        bs(n);
        break;
      case 1:
        Qe(n.type) && fl(n);
        break;
      case 4:
        ui(n, n.stateNode.containerInfo);
        break;
      case 10:
        var r = n.type._context, o = n.memoizedProps.value;
        le(gl, r._currentValue), r._currentValue = o;
        break;
      case 13:
        if (r = n.memoizedState, r !== null)
          return r.dehydrated !== null ? (le(ce, ce.current & 1), n.flags |= 128, null) : (t & n.child.childLanes) !== 0 ? ja(e, n, t) : (le(ce, ce.current & 1), e = On(e, n, t), e !== null ? e.sibling : null);
        le(ce, ce.current & 1);
        break;
      case 19:
        if (r = (t & n.childLanes) !== 0, (e.flags & 128) !== 0) {
          if (r) return Ua(e, n, t);
          n.flags |= 128;
        }
        if (o = n.memoizedState, o !== null && (o.rendering = null, o.tail = null, o.lastEffect = null), le(ce, ce.current), r) break;
        return null;
      case 22:
      case 23:
        return n.lanes = 0, Ra(e, n, t);
    }
    return On(e, n, t);
  }
  var Wa, Mi, Ha, Ba;
  Wa = function(e, n) {
    for (var t = n.child; t !== null; ) {
      if (t.tag === 5 || t.tag === 6) e.appendChild(t.stateNode);
      else if (t.tag !== 4 && t.child !== null) {
        t.child.return = t, t = t.child;
        continue;
      }
      if (t === n) break;
      for (; t.sibling === null; ) {
        if (t.return === null || t.return === n) return;
        t = t.return;
      }
      t.sibling.return = t.return, t = t.sibling;
    }
  }, Mi = function() {
  }, Ha = function(e, n, t, r) {
    var o = e.memoizedProps;
    if (o !== r) {
      e = n.stateNode, dt(_n.current);
      var i = null;
      switch (t) {
        case "input":
          o = ro(e, o), r = ro(e, r), i = [];
          break;
        case "select":
          o = D({}, o, { value: void 0 }), r = D({}, r, { value: void 0 }), i = [];
          break;
        case "textarea":
          o = io(e, o), r = io(e, r), i = [];
          break;
        default:
          typeof o.onClick != "function" && typeof r.onClick == "function" && (e.onclick = sl);
      }
      so(t, r);
      var a;
      t = null;
      for (w in o) if (!r.hasOwnProperty(w) && o.hasOwnProperty(w) && o[w] != null) if (w === "style") {
        var d = o[w];
        for (a in d) d.hasOwnProperty(a) && (t || (t = {}), t[a] = "");
      } else w !== "dangerouslySetInnerHTML" && w !== "children" && w !== "suppressContentEditableWarning" && w !== "suppressHydrationWarning" && w !== "autoFocus" && (f.hasOwnProperty(w) ? i || (i = []) : (i = i || []).push(w, null));
      for (w in r) {
        var p = r[w];
        if (d = o?.[w], r.hasOwnProperty(w) && p !== d && (p != null || d != null)) if (w === "style") if (d) {
          for (a in d) !d.hasOwnProperty(a) || p && p.hasOwnProperty(a) || (t || (t = {}), t[a] = "");
          for (a in p) p.hasOwnProperty(a) && d[a] !== p[a] && (t || (t = {}), t[a] = p[a]);
        } else t || (i || (i = []), i.push(
          w,
          t
        )), t = p;
        else w === "dangerouslySetInnerHTML" ? (p = p ? p.__html : void 0, d = d ? d.__html : void 0, p != null && d !== p && (i = i || []).push(w, p)) : w === "children" ? typeof p != "string" && typeof p != "number" || (i = i || []).push(w, "" + p) : w !== "suppressContentEditableWarning" && w !== "suppressHydrationWarning" && (f.hasOwnProperty(w) ? (p != null && w === "onScroll" && oe("scroll", e), i || d === p || (i = [])) : (i = i || []).push(w, p));
      }
      t && (i = i || []).push("style", t);
      var w = i;
      (n.updateQueue = w) && (n.flags |= 4);
    }
  }, Ba = function(e, n, t, r) {
    t !== r && (n.flags |= 4);
  };
  function Nr(e, n) {
    if (!ae) switch (e.tailMode) {
      case "hidden":
        n = e.tail;
        for (var t = null; n !== null; ) n.alternate !== null && (t = n), n = n.sibling;
        t === null ? e.tail = null : t.sibling = null;
        break;
      case "collapsed":
        t = e.tail;
        for (var r = null; t !== null; ) t.alternate !== null && (r = t), t = t.sibling;
        r === null ? n || e.tail === null ? e.tail = null : e.tail.sibling = null : r.sibling = null;
    }
  }
  function Fe(e) {
    var n = e.alternate !== null && e.alternate.child === e.child, t = 0, r = 0;
    if (n) for (var o = e.child; o !== null; ) t |= o.lanes | o.childLanes, r |= o.subtreeFlags & 14680064, r |= o.flags & 14680064, o.return = e, o = o.sibling;
    else for (o = e.child; o !== null; ) t |= o.lanes | o.childLanes, r |= o.subtreeFlags, r |= o.flags, o.return = e, o = o.sibling;
    return e.subtreeFlags |= r, e.childLanes = t, n;
  }
  function Ud(e, n, t) {
    var r = n.pendingProps;
    switch (Zo(n), n.tag) {
      case 2:
      case 16:
      case 15:
      case 0:
      case 11:
      case 7:
      case 8:
      case 12:
      case 9:
      case 14:
        return Fe(n), null;
      case 1:
        return Qe(n.type) && cl(), Fe(n), null;
      case 3:
        return r = n.stateNode, Bt(), ie($e), ie(Oe), ci(), r.pendingContext && (r.context = r.pendingContext, r.pendingContext = null), (e === null || e.child === null) && (ml(n) ? n.flags |= 4 : e === null || e.memoizedState.isDehydrated && (n.flags & 256) === 0 || (n.flags |= 1024, vn !== null && (Wi(vn), vn = null))), Mi(e, n), Fe(n), null;
      case 5:
        si(n);
        var o = dt(Cr.current);
        if (t = n.type, e !== null && n.stateNode != null) Ha(e, n, t, r, o), e.ref !== n.ref && (n.flags |= 512, n.flags |= 2097152);
        else {
          if (!r) {
            if (n.stateNode === null) throw Error(s(166));
            return Fe(n), null;
          }
          if (e = dt(_n.current), ml(n)) {
            r = n.stateNode, t = n.type;
            var i = n.memoizedProps;
            switch (r[En] = n, r[gr] = i, e = (n.mode & 1) !== 0, t) {
              case "dialog":
                oe("cancel", r), oe("close", r);
                break;
              case "iframe":
              case "object":
              case "embed":
                oe("load", r);
                break;
              case "video":
              case "audio":
                for (o = 0; o < hr.length; o++) oe(hr[o], r);
                break;
              case "source":
                oe("error", r);
                break;
              case "img":
              case "image":
              case "link":
                oe(
                  "error",
                  r
                ), oe("load", r);
                break;
              case "details":
                oe("toggle", r);
                break;
              case "input":
                Cu(r, i), oe("invalid", r);
                break;
              case "select":
                r._wrapperState = { wasMultiple: !!i.multiple }, oe("invalid", r);
                break;
              case "textarea":
                xu(r, i), oe("invalid", r);
            }
            so(t, i), o = null;
            for (var a in i) if (i.hasOwnProperty(a)) {
              var d = i[a];
              a === "children" ? typeof d == "string" ? r.textContent !== d && (i.suppressHydrationWarning !== !0 && ul(r.textContent, d, e), o = ["children", d]) : typeof d == "number" && r.textContent !== "" + d && (i.suppressHydrationWarning !== !0 && ul(
                r.textContent,
                d,
                e
              ), o = ["children", "" + d]) : f.hasOwnProperty(a) && d != null && a === "onScroll" && oe("scroll", r);
            }
            switch (t) {
              case "input":
                Ar(r), _u(r, i, !0);
                break;
              case "textarea":
                Ar(r), Nu(r);
                break;
              case "select":
              case "option":
                break;
              default:
                typeof i.onClick == "function" && (r.onclick = sl);
            }
            r = o, n.updateQueue = r, r !== null && (n.flags |= 4);
          } else {
            a = o.nodeType === 9 ? o : o.ownerDocument, e === "http://www.w3.org/1999/xhtml" && (e = zu(t)), e === "http://www.w3.org/1999/xhtml" ? t === "script" ? (e = a.createElement("div"), e.innerHTML = "<script><\/script>", e = e.removeChild(e.firstChild)) : typeof r.is == "string" ? e = a.createElement(t, { is: r.is }) : (e = a.createElement(t), t === "select" && (a = e, r.multiple ? a.multiple = !0 : r.size && (a.size = r.size))) : e = a.createElementNS(e, t), e[En] = n, e[gr] = r, Wa(e, n, !1, !1), n.stateNode = e;
            e: {
              switch (a = ao(t, r), t) {
                case "dialog":
                  oe("cancel", e), oe("close", e), o = r;
                  break;
                case "iframe":
                case "object":
                case "embed":
                  oe("load", e), o = r;
                  break;
                case "video":
                case "audio":
                  for (o = 0; o < hr.length; o++) oe(hr[o], e);
                  o = r;
                  break;
                case "source":
                  oe("error", e), o = r;
                  break;
                case "img":
                case "image":
                case "link":
                  oe(
                    "error",
                    e
                  ), oe("load", e), o = r;
                  break;
                case "details":
                  oe("toggle", e), o = r;
                  break;
                case "input":
                  Cu(e, r), o = ro(e, r), oe("invalid", e);
                  break;
                case "option":
                  o = r;
                  break;
                case "select":
                  e._wrapperState = { wasMultiple: !!r.multiple }, o = D({}, r, { value: void 0 }), oe("invalid", e);
                  break;
                case "textarea":
                  xu(e, r), o = io(e, r), oe("invalid", e);
                  break;
                default:
                  o = r;
              }
              so(t, o), d = o;
              for (i in d) if (d.hasOwnProperty(i)) {
                var p = d[i];
                i === "style" ? Lu(e, p) : i === "dangerouslySetInnerHTML" ? (p = p ? p.__html : void 0, p != null && Mu(e, p)) : i === "children" ? typeof p == "string" ? (t !== "textarea" || p !== "") && Xt(e, p) : typeof p == "number" && Xt(e, "" + p) : i !== "suppressContentEditableWarning" && i !== "suppressHydrationWarning" && i !== "autoFocus" && (f.hasOwnProperty(i) ? p != null && i === "onScroll" && oe("scroll", e) : p != null && Le(e, i, p, a));
              }
              switch (t) {
                case "input":
                  Ar(e), _u(e, r, !1);
                  break;
                case "textarea":
                  Ar(e), Nu(e);
                  break;
                case "option":
                  r.value != null && e.setAttribute("value", "" + ne(r.value));
                  break;
                case "select":
                  e.multiple = !!r.multiple, i = r.value, i != null ? Et(e, !!r.multiple, i, !1) : r.defaultValue != null && Et(
                    e,
                    !!r.multiple,
                    r.defaultValue,
                    !0
                  );
                  break;
                default:
                  typeof o.onClick == "function" && (e.onclick = sl);
              }
              switch (t) {
                case "button":
                case "input":
                case "select":
                case "textarea":
                  r = !!r.autoFocus;
                  break e;
                case "img":
                  r = !0;
                  break e;
                default:
                  r = !1;
              }
            }
            r && (n.flags |= 4);
          }
          n.ref !== null && (n.flags |= 512, n.flags |= 2097152);
        }
        return Fe(n), null;
      case 6:
        if (e && n.stateNode != null) Ba(e, n, e.memoizedProps, r);
        else {
          if (typeof r != "string" && n.stateNode === null) throw Error(s(166));
          if (t = dt(Cr.current), dt(_n.current), ml(n)) {
            if (r = n.stateNode, t = n.memoizedProps, r[En] = n, (i = r.nodeValue !== t) && (e = nn, e !== null)) switch (e.tag) {
              case 3:
                ul(r.nodeValue, t, (e.mode & 1) !== 0);
                break;
              case 5:
                e.memoizedProps.suppressHydrationWarning !== !0 && ul(r.nodeValue, t, (e.mode & 1) !== 0);
            }
            i && (n.flags |= 4);
          } else r = (t.nodeType === 9 ? t : t.ownerDocument).createTextNode(r), r[En] = n, n.stateNode = r;
        }
        return Fe(n), null;
      case 13:
        if (ie(ce), r = n.memoizedState, e === null || e.memoizedState !== null && e.memoizedState.dehydrated !== null) {
          if (ae && tn !== null && (n.mode & 1) !== 0 && (n.flags & 128) === 0) Qs(), At(), n.flags |= 98560, i = !1;
          else if (i = ml(n), r !== null && r.dehydrated !== null) {
            if (e === null) {
              if (!i) throw Error(s(318));
              if (i = n.memoizedState, i = i !== null ? i.dehydrated : null, !i) throw Error(s(317));
              i[En] = n;
            } else At(), (n.flags & 128) === 0 && (n.memoizedState = null), n.flags |= 4;
            Fe(n), i = !1;
          } else vn !== null && (Wi(vn), vn = null), i = !0;
          if (!i) return n.flags & 65536 ? n : null;
        }
        return (n.flags & 128) !== 0 ? (n.lanes = t, n) : (r = r !== null, r !== (e !== null && e.memoizedState !== null) && r && (n.child.flags |= 8192, (n.mode & 1) !== 0 && (e === null || (ce.current & 1) !== 0 ? xe === 0 && (xe = 3) : Vi())), n.updateQueue !== null && (n.flags |= 4), Fe(n), null);
      case 4:
        return Bt(), Mi(e, n), e === null && mr(n.stateNode.containerInfo), Fe(n), null;
      case 10:
        return ri(n.type._context), Fe(n), null;
      case 17:
        return Qe(n.type) && cl(), Fe(n), null;
      case 19:
        if (ie(ce), i = n.memoizedState, i === null) return Fe(n), null;
        if (r = (n.flags & 128) !== 0, a = i.rendering, a === null) if (r) Nr(i, !1);
        else {
          if (xe !== 0 || e !== null && (e.flags & 128) !== 0) for (e = n.child; e !== null; ) {
            if (a = Sl(e), a !== null) {
              for (n.flags |= 128, Nr(i, !1), r = a.updateQueue, r !== null && (n.updateQueue = r, n.flags |= 4), n.subtreeFlags = 0, r = t, t = n.child; t !== null; ) i = t, e = r, i.flags &= 14680066, a = i.alternate, a === null ? (i.childLanes = 0, i.lanes = e, i.child = null, i.subtreeFlags = 0, i.memoizedProps = null, i.memoizedState = null, i.updateQueue = null, i.dependencies = null, i.stateNode = null) : (i.childLanes = a.childLanes, i.lanes = a.lanes, i.child = a.child, i.subtreeFlags = 0, i.deletions = null, i.memoizedProps = a.memoizedProps, i.memoizedState = a.memoizedState, i.updateQueue = a.updateQueue, i.type = a.type, e = a.dependencies, i.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }), t = t.sibling;
              return le(ce, ce.current & 1 | 2), n.child;
            }
            e = e.sibling;
          }
          i.tail !== null && ge() > Kt && (n.flags |= 128, r = !0, Nr(i, !1), n.lanes = 4194304);
        }
        else {
          if (!r) if (e = Sl(a), e !== null) {
            if (n.flags |= 128, r = !0, t = e.updateQueue, t !== null && (n.updateQueue = t, n.flags |= 4), Nr(i, !0), i.tail === null && i.tailMode === "hidden" && !a.alternate && !ae) return Fe(n), null;
          } else 2 * ge() - i.renderingStartTime > Kt && t !== 1073741824 && (n.flags |= 128, r = !0, Nr(i, !1), n.lanes = 4194304);
          i.isBackwards ? (a.sibling = n.child, n.child = a) : (t = i.last, t !== null ? t.sibling = a : n.child = a, i.last = a);
        }
        return i.tail !== null ? (n = i.tail, i.rendering = n, i.tail = n.sibling, i.renderingStartTime = ge(), n.sibling = null, t = ce.current, le(ce, r ? t & 1 | 2 : t & 1), n) : (Fe(n), null);
      case 22:
      case 23:
        return Bi(), r = n.memoizedState !== null, e !== null && e.memoizedState !== null !== r && (n.flags |= 8192), r && (n.mode & 1) !== 0 ? (rn & 1073741824) !== 0 && (Fe(n), n.subtreeFlags & 6 && (n.flags |= 8192)) : Fe(n), null;
      case 24:
        return null;
      case 25:
        return null;
    }
    throw Error(s(156, n.tag));
  }
  function Wd(e, n) {
    switch (Zo(n), n.tag) {
      case 1:
        return Qe(n.type) && cl(), e = n.flags, e & 65536 ? (n.flags = e & -65537 | 128, n) : null;
      case 3:
        return Bt(), ie($e), ie(Oe), ci(), e = n.flags, (e & 65536) !== 0 && (e & 128) === 0 ? (n.flags = e & -65537 | 128, n) : null;
      case 5:
        return si(n), null;
      case 13:
        if (ie(ce), e = n.memoizedState, e !== null && e.dehydrated !== null) {
          if (n.alternate === null) throw Error(s(340));
          At();
        }
        return e = n.flags, e & 65536 ? (n.flags = e & -65537 | 128, n) : null;
      case 19:
        return ie(ce), null;
      case 4:
        return Bt(), null;
      case 10:
        return ri(n.type._context), null;
      case 22:
      case 23:
        return Bi(), null;
      case 24:
        return null;
      default:
        return null;
    }
  }
  var Tl = !1, je = !1, Hd = typeof WeakSet == "function" ? WeakSet : Set, R = null;
  function $t(e, n) {
    var t = e.ref;
    if (t !== null) if (typeof t == "function") try {
      t(null);
    } catch (r) {
      me(e, n, r);
    }
    else t.current = null;
  }
  function Ti(e, n, t) {
    try {
      t();
    } catch (r) {
      me(e, n, r);
    }
  }
  var Va = !1;
  function Bd(e, n) {
    if (Bo = Gr, e = Ss(), Oo(e)) {
      if ("selectionStart" in e) var t = { start: e.selectionStart, end: e.selectionEnd };
      else e: {
        t = (t = e.ownerDocument) && t.defaultView || window;
        var r = t.getSelection && t.getSelection();
        if (r && r.rangeCount !== 0) {
          t = r.anchorNode;
          var o = r.anchorOffset, i = r.focusNode;
          r = r.focusOffset;
          try {
            t.nodeType, i.nodeType;
          } catch {
            t = null;
            break e;
          }
          var a = 0, d = -1, p = -1, w = 0, x = 0, P = e, C = null;
          n: for (; ; ) {
            for (var L; P !== t || o !== 0 && P.nodeType !== 3 || (d = a + o), P !== i || r !== 0 && P.nodeType !== 3 || (p = a + r), P.nodeType === 3 && (a += P.nodeValue.length), (L = P.firstChild) !== null; )
              C = P, P = L;
            for (; ; ) {
              if (P === e) break n;
              if (C === t && ++w === o && (d = a), C === i && ++x === r && (p = a), (L = P.nextSibling) !== null) break;
              P = C, C = P.parentNode;
            }
            P = L;
          }
          t = d === -1 || p === -1 ? null : { start: d, end: p };
        } else t = null;
      }
      t = t || { start: 0, end: 0 };
    } else t = null;
    for (Vo = { focusedElem: e, selectionRange: t }, Gr = !1, R = n; R !== null; ) if (n = R, e = n.child, (n.subtreeFlags & 1028) !== 0 && e !== null) e.return = n, R = e;
    else for (; R !== null; ) {
      n = R;
      try {
        var I = n.alternate;
        if ((n.flags & 1024) !== 0) switch (n.tag) {
          case 0:
          case 11:
          case 15:
            break;
          case 1:
            if (I !== null) {
              var F = I.memoizedProps, ye = I.memoizedState, g = n.stateNode, h = g.getSnapshotBeforeUpdate(n.elementType === n.type ? F : gn(n.type, F), ye);
              g.__reactInternalSnapshotBeforeUpdate = h;
            }
            break;
          case 3:
            var y = n.stateNode.containerInfo;
            y.nodeType === 1 ? y.textContent = "" : y.nodeType === 9 && y.documentElement && y.removeChild(y.documentElement);
            break;
          case 5:
          case 6:
          case 4:
          case 17:
            break;
          default:
            throw Error(s(163));
        }
      } catch (N) {
        me(n, n.return, N);
      }
      if (e = n.sibling, e !== null) {
        e.return = n.return, R = e;
        break;
      }
      R = n.return;
    }
    return I = Va, Va = !1, I;
  }
  function zr(e, n, t) {
    var r = n.updateQueue;
    if (r = r !== null ? r.lastEffect : null, r !== null) {
      var o = r = r.next;
      do {
        if ((o.tag & e) === e) {
          var i = o.destroy;
          o.destroy = void 0, i !== void 0 && Ti(n, t, i);
        }
        o = o.next;
      } while (o !== r);
    }
  }
  function Ll(e, n) {
    if (n = n.updateQueue, n = n !== null ? n.lastEffect : null, n !== null) {
      var t = n = n.next;
      do {
        if ((t.tag & e) === e) {
          var r = t.create;
          t.destroy = r();
        }
        t = t.next;
      } while (t !== n);
    }
  }
  function Li(e) {
    var n = e.ref;
    if (n !== null) {
      var t = e.stateNode;
      e.tag, e = t, typeof n == "function" ? n(e) : n.current = e;
    }
  }
  function $a(e) {
    var n = e.alternate;
    n !== null && (e.alternate = null, $a(n)), e.child = null, e.deletions = null, e.sibling = null, e.tag === 5 && (n = e.stateNode, n !== null && (delete n[En], delete n[gr], delete n[Yo], delete n[_d], delete n[xd])), e.stateNode = null, e.return = null, e.dependencies = null, e.memoizedProps = null, e.memoizedState = null, e.pendingProps = null, e.stateNode = null, e.updateQueue = null;
  }
  function Qa(e) {
    return e.tag === 5 || e.tag === 3 || e.tag === 4;
  }
  function Ka(e) {
    e: for (; ; ) {
      for (; e.sibling === null; ) {
        if (e.return === null || Qa(e.return)) return null;
        e = e.return;
      }
      for (e.sibling.return = e.return, e = e.sibling; e.tag !== 5 && e.tag !== 6 && e.tag !== 18; ) {
        if (e.flags & 2 || e.child === null || e.tag === 4) continue e;
        e.child.return = e, e = e.child;
      }
      if (!(e.flags & 2)) return e.stateNode;
    }
  }
  function Ri(e, n, t) {
    var r = e.tag;
    if (r === 5 || r === 6) e = e.stateNode, n ? t.nodeType === 8 ? t.parentNode.insertBefore(e, n) : t.insertBefore(e, n) : (t.nodeType === 8 ? (n = t.parentNode, n.insertBefore(e, t)) : (n = t, n.appendChild(e)), t = t._reactRootContainer, t != null || n.onclick !== null || (n.onclick = sl));
    else if (r !== 4 && (e = e.child, e !== null)) for (Ri(e, n, t), e = e.sibling; e !== null; ) Ri(e, n, t), e = e.sibling;
  }
  function Di(e, n, t) {
    var r = e.tag;
    if (r === 5 || r === 6) e = e.stateNode, n ? t.insertBefore(e, n) : t.appendChild(e);
    else if (r !== 4 && (e = e.child, e !== null)) for (Di(e, n, t), e = e.sibling; e !== null; ) Di(e, n, t), e = e.sibling;
  }
  var Re = null, yn = !1;
  function Gn(e, n, t) {
    for (t = t.child; t !== null; ) Ya(e, n, t), t = t.sibling;
  }
  function Ya(e, n, t) {
    if (Cn && typeof Cn.onCommitFiberUnmount == "function") try {
      Cn.onCommitFiberUnmount($r, t);
    } catch {
    }
    switch (t.tag) {
      case 5:
        je || $t(t, n);
      case 6:
        var r = Re, o = yn;
        Re = null, Gn(e, n, t), Re = r, yn = o, Re !== null && (yn ? (e = Re, t = t.stateNode, e.nodeType === 8 ? e.parentNode.removeChild(t) : e.removeChild(t)) : Re.removeChild(t.stateNode));
        break;
      case 18:
        Re !== null && (yn ? (e = Re, t = t.stateNode, e.nodeType === 8 ? Ko(e.parentNode, t) : e.nodeType === 1 && Ko(e, t), ir(e)) : Ko(Re, t.stateNode));
        break;
      case 4:
        r = Re, o = yn, Re = t.stateNode.containerInfo, yn = !0, Gn(e, n, t), Re = r, yn = o;
        break;
      case 0:
      case 11:
      case 14:
      case 15:
        if (!je && (r = t.updateQueue, r !== null && (r = r.lastEffect, r !== null))) {
          o = r = r.next;
          do {
            var i = o, a = i.destroy;
            i = i.tag, a !== void 0 && ((i & 2) !== 0 || (i & 4) !== 0) && Ti(t, n, a), o = o.next;
          } while (o !== r);
        }
        Gn(e, n, t);
        break;
      case 1:
        if (!je && ($t(t, n), r = t.stateNode, typeof r.componentWillUnmount == "function")) try {
          r.props = t.memoizedProps, r.state = t.memoizedState, r.componentWillUnmount();
        } catch (d) {
          me(t, n, d);
        }
        Gn(e, n, t);
        break;
      case 21:
        Gn(e, n, t);
        break;
      case 22:
        t.mode & 1 ? (je = (r = je) || t.memoizedState !== null, Gn(e, n, t), je = r) : Gn(e, n, t);
        break;
      default:
        Gn(e, n, t);
    }
  }
  function qa(e) {
    var n = e.updateQueue;
    if (n !== null) {
      e.updateQueue = null;
      var t = e.stateNode;
      t === null && (t = e.stateNode = new Hd()), n.forEach(function(r) {
        var o = Zd.bind(null, e, r);
        t.has(r) || (t.add(r), r.then(o, o));
      });
    }
  }
  function wn(e, n) {
    var t = n.deletions;
    if (t !== null) for (var r = 0; r < t.length; r++) {
      var o = t[r];
      try {
        var i = e, a = n, d = a;
        e: for (; d !== null; ) {
          switch (d.tag) {
            case 5:
              Re = d.stateNode, yn = !1;
              break e;
            case 3:
              Re = d.stateNode.containerInfo, yn = !0;
              break e;
            case 4:
              Re = d.stateNode.containerInfo, yn = !0;
              break e;
          }
          d = d.return;
        }
        if (Re === null) throw Error(s(160));
        Ya(i, a, o), Re = null, yn = !1;
        var p = o.alternate;
        p !== null && (p.return = null), o.return = null;
      } catch (w) {
        me(o, n, w);
      }
    }
    if (n.subtreeFlags & 12854) for (n = n.child; n !== null; ) Xa(n, e), n = n.sibling;
  }
  function Xa(e, n) {
    var t = e.alternate, r = e.flags;
    switch (e.tag) {
      case 0:
      case 11:
      case 14:
      case 15:
        if (wn(n, e), Pn(e), r & 4) {
          try {
            zr(3, e, e.return), Ll(3, e);
          } catch (F) {
            me(e, e.return, F);
          }
          try {
            zr(5, e, e.return);
          } catch (F) {
            me(e, e.return, F);
          }
        }
        break;
      case 1:
        wn(n, e), Pn(e), r & 512 && t !== null && $t(t, t.return);
        break;
      case 5:
        if (wn(n, e), Pn(e), r & 512 && t !== null && $t(t, t.return), e.flags & 32) {
          var o = e.stateNode;
          try {
            Xt(o, "");
          } catch (F) {
            me(e, e.return, F);
          }
        }
        if (r & 4 && (o = e.stateNode, o != null)) {
          var i = e.memoizedProps, a = t !== null ? t.memoizedProps : i, d = e.type, p = e.updateQueue;
          if (e.updateQueue = null, p !== null) try {
            d === "input" && i.type === "radio" && i.name != null && Eu(o, i), ao(d, a);
            var w = ao(d, i);
            for (a = 0; a < p.length; a += 2) {
              var x = p[a], P = p[a + 1];
              x === "style" ? Lu(o, P) : x === "dangerouslySetInnerHTML" ? Mu(o, P) : x === "children" ? Xt(o, P) : Le(o, x, P, w);
            }
            switch (d) {
              case "input":
                lo(o, i);
                break;
              case "textarea":
                Pu(o, i);
                break;
              case "select":
                var C = o._wrapperState.wasMultiple;
                o._wrapperState.wasMultiple = !!i.multiple;
                var L = i.value;
                L != null ? Et(o, !!i.multiple, L, !1) : C !== !!i.multiple && (i.defaultValue != null ? Et(
                  o,
                  !!i.multiple,
                  i.defaultValue,
                  !0
                ) : Et(o, !!i.multiple, i.multiple ? [] : "", !1));
            }
            o[gr] = i;
          } catch (F) {
            me(e, e.return, F);
          }
        }
        break;
      case 6:
        if (wn(n, e), Pn(e), r & 4) {
          if (e.stateNode === null) throw Error(s(162));
          o = e.stateNode, i = e.memoizedProps;
          try {
            o.nodeValue = i;
          } catch (F) {
            me(e, e.return, F);
          }
        }
        break;
      case 3:
        if (wn(n, e), Pn(e), r & 4 && t !== null && t.memoizedState.isDehydrated) try {
          ir(n.containerInfo);
        } catch (F) {
          me(e, e.return, F);
        }
        break;
      case 4:
        wn(n, e), Pn(e);
        break;
      case 13:
        wn(n, e), Pn(e), o = e.child, o.flags & 8192 && (i = o.memoizedState !== null, o.stateNode.isHidden = i, !i || o.alternate !== null && o.alternate.memoizedState !== null || (Fi = ge())), r & 4 && qa(e);
        break;
      case 22:
        if (x = t !== null && t.memoizedState !== null, e.mode & 1 ? (je = (w = je) || x, wn(n, e), je = w) : wn(n, e), Pn(e), r & 8192) {
          if (w = e.memoizedState !== null, (e.stateNode.isHidden = w) && !x && (e.mode & 1) !== 0) for (R = e, x = e.child; x !== null; ) {
            for (P = R = x; R !== null; ) {
              switch (C = R, L = C.child, C.tag) {
                case 0:
                case 11:
                case 14:
                case 15:
                  zr(4, C, C.return);
                  break;
                case 1:
                  $t(C, C.return);
                  var I = C.stateNode;
                  if (typeof I.componentWillUnmount == "function") {
                    r = C, t = C.return;
                    try {
                      n = r, I.props = n.memoizedProps, I.state = n.memoizedState, I.componentWillUnmount();
                    } catch (F) {
                      me(r, t, F);
                    }
                  }
                  break;
                case 5:
                  $t(C, C.return);
                  break;
                case 22:
                  if (C.memoizedState !== null) {
                    Ja(P);
                    continue;
                  }
              }
              L !== null ? (L.return = C, R = L) : Ja(P);
            }
            x = x.sibling;
          }
          e: for (x = null, P = e; ; ) {
            if (P.tag === 5) {
              if (x === null) {
                x = P;
                try {
                  o = P.stateNode, w ? (i = o.style, typeof i.setProperty == "function" ? i.setProperty("display", "none", "important") : i.display = "none") : (d = P.stateNode, p = P.memoizedProps.style, a = p != null && p.hasOwnProperty("display") ? p.display : null, d.style.display = Tu("display", a));
                } catch (F) {
                  me(e, e.return, F);
                }
              }
            } else if (P.tag === 6) {
              if (x === null) try {
                P.stateNode.nodeValue = w ? "" : P.memoizedProps;
              } catch (F) {
                me(e, e.return, F);
              }
            } else if ((P.tag !== 22 && P.tag !== 23 || P.memoizedState === null || P === e) && P.child !== null) {
              P.child.return = P, P = P.child;
              continue;
            }
            if (P === e) break e;
            for (; P.sibling === null; ) {
              if (P.return === null || P.return === e) break e;
              x === P && (x = null), P = P.return;
            }
            x === P && (x = null), P.sibling.return = P.return, P = P.sibling;
          }
        }
        break;
      case 19:
        wn(n, e), Pn(e), r & 4 && qa(e);
        break;
      case 21:
        break;
      default:
        wn(
          n,
          e
        ), Pn(e);
    }
  }
  function Pn(e) {
    var n = e.flags;
    if (n & 2) {
      try {
        e: {
          for (var t = e.return; t !== null; ) {
            if (Qa(t)) {
              var r = t;
              break e;
            }
            t = t.return;
          }
          throw Error(s(160));
        }
        switch (r.tag) {
          case 5:
            var o = r.stateNode;
            r.flags & 32 && (Xt(o, ""), r.flags &= -33);
            var i = Ka(e);
            Di(e, i, o);
            break;
          case 3:
          case 4:
            var a = r.stateNode.containerInfo, d = Ka(e);
            Ri(e, d, a);
            break;
          default:
            throw Error(s(161));
        }
      } catch (p) {
        me(e, e.return, p);
      }
      e.flags &= -3;
    }
    n & 4096 && (e.flags &= -4097);
  }
  function Vd(e, n, t) {
    R = e, Ga(e);
  }
  function Ga(e, n, t) {
    for (var r = (e.mode & 1) !== 0; R !== null; ) {
      var o = R, i = o.child;
      if (o.tag === 22 && r) {
        var a = o.memoizedState !== null || Tl;
        if (!a) {
          var d = o.alternate, p = d !== null && d.memoizedState !== null || je;
          d = Tl;
          var w = je;
          if (Tl = a, (je = p) && !w) for (R = o; R !== null; ) a = R, p = a.child, a.tag === 22 && a.memoizedState !== null ? ba(o) : p !== null ? (p.return = a, R = p) : ba(o);
          for (; i !== null; ) R = i, Ga(i), i = i.sibling;
          R = o, Tl = d, je = w;
        }
        Za(e);
      } else (o.subtreeFlags & 8772) !== 0 && i !== null ? (i.return = o, R = i) : Za(e);
    }
  }
  function Za(e) {
    for (; R !== null; ) {
      var n = R;
      if ((n.flags & 8772) !== 0) {
        var t = n.alternate;
        try {
          if ((n.flags & 8772) !== 0) switch (n.tag) {
            case 0:
            case 11:
            case 15:
              je || Ll(5, n);
              break;
            case 1:
              var r = n.stateNode;
              if (n.flags & 4 && !je) if (t === null) r.componentDidMount();
              else {
                var o = n.elementType === n.type ? t.memoizedProps : gn(n.type, t.memoizedProps);
                r.componentDidUpdate(o, t.memoizedState, r.__reactInternalSnapshotBeforeUpdate);
              }
              var i = n.updateQueue;
              i !== null && Js(n, i, r);
              break;
            case 3:
              var a = n.updateQueue;
              if (a !== null) {
                if (t = null, n.child !== null) switch (n.child.tag) {
                  case 5:
                    t = n.child.stateNode;
                    break;
                  case 1:
                    t = n.child.stateNode;
                }
                Js(n, a, t);
              }
              break;
            case 5:
              var d = n.stateNode;
              if (t === null && n.flags & 4) {
                t = d;
                var p = n.memoizedProps;
                switch (n.type) {
                  case "button":
                  case "input":
                  case "select":
                  case "textarea":
                    p.autoFocus && t.focus();
                    break;
                  case "img":
                    p.src && (t.src = p.src);
                }
              }
              break;
            case 6:
              break;
            case 4:
              break;
            case 12:
              break;
            case 13:
              if (n.memoizedState === null) {
                var w = n.alternate;
                if (w !== null) {
                  var x = w.memoizedState;
                  if (x !== null) {
                    var P = x.dehydrated;
                    P !== null && ir(P);
                  }
                }
              }
              break;
            case 19:
            case 17:
            case 21:
            case 22:
            case 23:
            case 25:
              break;
            default:
              throw Error(s(163));
          }
          je || n.flags & 512 && Li(n);
        } catch (C) {
          me(n, n.return, C);
        }
      }
      if (n === e) {
        R = null;
        break;
      }
      if (t = n.sibling, t !== null) {
        t.return = n.return, R = t;
        break;
      }
      R = n.return;
    }
  }
  function Ja(e) {
    for (; R !== null; ) {
      var n = R;
      if (n === e) {
        R = null;
        break;
      }
      var t = n.sibling;
      if (t !== null) {
        t.return = n.return, R = t;
        break;
      }
      R = n.return;
    }
  }
  function ba(e) {
    for (; R !== null; ) {
      var n = R;
      try {
        switch (n.tag) {
          case 0:
          case 11:
          case 15:
            var t = n.return;
            try {
              Ll(4, n);
            } catch (p) {
              me(n, t, p);
            }
            break;
          case 1:
            var r = n.stateNode;
            if (typeof r.componentDidMount == "function") {
              var o = n.return;
              try {
                r.componentDidMount();
              } catch (p) {
                me(n, o, p);
              }
            }
            var i = n.return;
            try {
              Li(n);
            } catch (p) {
              me(n, i, p);
            }
            break;
          case 5:
            var a = n.return;
            try {
              Li(n);
            } catch (p) {
              me(n, a, p);
            }
        }
      } catch (p) {
        me(n, n.return, p);
      }
      if (n === e) {
        R = null;
        break;
      }
      var d = n.sibling;
      if (d !== null) {
        d.return = n.return, R = d;
        break;
      }
      R = n.return;
    }
  }
  var $d = Math.ceil, Rl = we.ReactCurrentDispatcher, Oi = we.ReactCurrentOwner, an = we.ReactCurrentBatchConfig, Z = 0, Me = null, Se = null, De = 0, rn = 0, Qt = Qn(0), xe = 0, Mr = null, ht = 0, Dl = 0, Ii = 0, Tr = null, Ye = null, Fi = 0, Kt = 1 / 0, In = null, Ol = !1, ji = null, Zn = null, Il = !1, Jn = null, Fl = 0, Lr = 0, Ai = null, jl = -1, Al = 0;
  function We() {
    return (Z & 6) !== 0 ? ge() : jl !== -1 ? jl : jl = ge();
  }
  function bn(e) {
    return (e.mode & 1) === 0 ? 1 : (Z & 2) !== 0 && De !== 0 ? De & -De : Nd.transition !== null ? (Al === 0 && (Al = Ku()), Al) : (e = te, e !== 0 || (e = window.event, e = e === void 0 ? 16 : ns(e.type)), e);
  }
  function kn(e, n, t, r) {
    if (50 < Lr) throw Lr = 0, Ai = null, Error(s(185));
    nr(e, t, r), ((Z & 2) === 0 || e !== Me) && (e === Me && ((Z & 2) === 0 && (Dl |= t), xe === 4 && et(e, De)), qe(e, r), t === 1 && Z === 0 && (n.mode & 1) === 0 && (Kt = ge() + 500, dl && Yn()));
  }
  function qe(e, n) {
    var t = e.callbackNode;
    Nf(e, n);
    var r = Yr(e, e === Me ? De : 0);
    if (r === 0) t !== null && Vu(t), e.callbackNode = null, e.callbackPriority = 0;
    else if (n = r & -r, e.callbackPriority !== n) {
      if (t != null && Vu(t), n === 1) e.tag === 0 ? Pd(nc.bind(null, e)) : Ws(nc.bind(null, e)), Cd(function() {
        (Z & 6) === 0 && Yn();
      }), t = null;
      else {
        switch (Yu(r)) {
          case 1:
            t = go;
            break;
          case 4:
            t = $u;
            break;
          case 16:
            t = Vr;
            break;
          case 536870912:
            t = Qu;
            break;
          default:
            t = Vr;
        }
        t = ac(t, ec.bind(null, e));
      }
      e.callbackPriority = n, e.callbackNode = t;
    }
  }
  function ec(e, n) {
    if (jl = -1, Al = 0, (Z & 6) !== 0) throw Error(s(327));
    var t = e.callbackNode;
    if (Yt() && e.callbackNode !== t) return null;
    var r = Yr(e, e === Me ? De : 0);
    if (r === 0) return null;
    if ((r & 30) !== 0 || (r & e.expiredLanes) !== 0 || n) n = Ul(e, r);
    else {
      n = r;
      var o = Z;
      Z |= 2;
      var i = rc();
      (Me !== e || De !== n) && (In = null, Kt = ge() + 500, vt(e, n));
      do
        try {
          Yd();
          break;
        } catch (d) {
          tc(e, d);
        }
      while (!0);
      ti(), Rl.current = i, Z = o, Se !== null ? n = 0 : (Me = null, De = 0, n = xe);
    }
    if (n !== 0) {
      if (n === 2 && (o = yo(e), o !== 0 && (r = o, n = Ui(e, o))), n === 1) throw t = Mr, vt(e, 0), et(e, r), qe(e, ge()), t;
      if (n === 6) et(e, r);
      else {
        if (o = e.current.alternate, (r & 30) === 0 && !Qd(o) && (n = Ul(e, r), n === 2 && (i = yo(e), i !== 0 && (r = i, n = Ui(e, i))), n === 1)) throw t = Mr, vt(e, 0), et(e, r), qe(e, ge()), t;
        switch (e.finishedWork = o, e.finishedLanes = r, n) {
          case 0:
          case 1:
            throw Error(s(345));
          case 2:
            gt(e, Ye, In);
            break;
          case 3:
            if (et(e, r), (r & 130023424) === r && (n = Fi + 500 - ge(), 10 < n)) {
              if (Yr(e, 0) !== 0) break;
              if (o = e.suspendedLanes, (o & r) !== r) {
                We(), e.pingedLanes |= e.suspendedLanes & o;
                break;
              }
              e.timeoutHandle = Qo(gt.bind(null, e, Ye, In), n);
              break;
            }
            gt(e, Ye, In);
            break;
          case 4:
            if (et(e, r), (r & 4194240) === r) break;
            for (n = e.eventTimes, o = -1; 0 < r; ) {
              var a = 31 - hn(r);
              i = 1 << a, a = n[a], a > o && (o = a), r &= ~i;
            }
            if (r = o, r = ge() - r, r = (120 > r ? 120 : 480 > r ? 480 : 1080 > r ? 1080 : 1920 > r ? 1920 : 3e3 > r ? 3e3 : 4320 > r ? 4320 : 1960 * $d(r / 1960)) - r, 10 < r) {
              e.timeoutHandle = Qo(gt.bind(null, e, Ye, In), r);
              break;
            }
            gt(e, Ye, In);
            break;
          case 5:
            gt(e, Ye, In);
            break;
          default:
            throw Error(s(329));
        }
      }
    }
    return qe(e, ge()), e.callbackNode === t ? ec.bind(null, e) : null;
  }
  function Ui(e, n) {
    var t = Tr;
    return e.current.memoizedState.isDehydrated && (vt(e, n).flags |= 256), e = Ul(e, n), e !== 2 && (n = Ye, Ye = t, n !== null && Wi(n)), e;
  }
  function Wi(e) {
    Ye === null ? Ye = e : Ye.push.apply(Ye, e);
  }
  function Qd(e) {
    for (var n = e; ; ) {
      if (n.flags & 16384) {
        var t = n.updateQueue;
        if (t !== null && (t = t.stores, t !== null)) for (var r = 0; r < t.length; r++) {
          var o = t[r], i = o.getSnapshot;
          o = o.value;
          try {
            if (!mn(i(), o)) return !1;
          } catch {
            return !1;
          }
        }
      }
      if (t = n.child, n.subtreeFlags & 16384 && t !== null) t.return = n, n = t;
      else {
        if (n === e) break;
        for (; n.sibling === null; ) {
          if (n.return === null || n.return === e) return !0;
          n = n.return;
        }
        n.sibling.return = n.return, n = n.sibling;
      }
    }
    return !0;
  }
  function et(e, n) {
    for (n &= ~Ii, n &= ~Dl, e.suspendedLanes |= n, e.pingedLanes &= ~n, e = e.expirationTimes; 0 < n; ) {
      var t = 31 - hn(n), r = 1 << t;
      e[t] = -1, n &= ~r;
    }
  }
  function nc(e) {
    if ((Z & 6) !== 0) throw Error(s(327));
    Yt();
    var n = Yr(e, 0);
    if ((n & 1) === 0) return qe(e, ge()), null;
    var t = Ul(e, n);
    if (e.tag !== 0 && t === 2) {
      var r = yo(e);
      r !== 0 && (n = r, t = Ui(e, r));
    }
    if (t === 1) throw t = Mr, vt(e, 0), et(e, n), qe(e, ge()), t;
    if (t === 6) throw Error(s(345));
    return e.finishedWork = e.current.alternate, e.finishedLanes = n, gt(e, Ye, In), qe(e, ge()), null;
  }
  function Hi(e, n) {
    var t = Z;
    Z |= 1;
    try {
      return e(n);
    } finally {
      Z = t, Z === 0 && (Kt = ge() + 500, dl && Yn());
    }
  }
  function mt(e) {
    Jn !== null && Jn.tag === 0 && (Z & 6) === 0 && Yt();
    var n = Z;
    Z |= 1;
    var t = an.transition, r = te;
    try {
      if (an.transition = null, te = 1, e) return e();
    } finally {
      te = r, an.transition = t, Z = n, (Z & 6) === 0 && Yn();
    }
  }
  function Bi() {
    rn = Qt.current, ie(Qt);
  }
  function vt(e, n) {
    e.finishedWork = null, e.finishedLanes = 0;
    var t = e.timeoutHandle;
    if (t !== -1 && (e.timeoutHandle = -1, Sd(t)), Se !== null) for (t = Se.return; t !== null; ) {
      var r = t;
      switch (Zo(r), r.tag) {
        case 1:
          r = r.type.childContextTypes, r != null && cl();
          break;
        case 3:
          Bt(), ie($e), ie(Oe), ci();
          break;
        case 5:
          si(r);
          break;
        case 4:
          Bt();
          break;
        case 13:
          ie(ce);
          break;
        case 19:
          ie(ce);
          break;
        case 10:
          ri(r.type._context);
          break;
        case 22:
        case 23:
          Bi();
      }
      t = t.return;
    }
    if (Me = e, Se = e = nt(e.current, null), De = rn = n, xe = 0, Mr = null, Ii = Dl = ht = 0, Ye = Tr = null, ft !== null) {
      for (n = 0; n < ft.length; n++) if (t = ft[n], r = t.interleaved, r !== null) {
        t.interleaved = null;
        var o = r.next, i = t.pending;
        if (i !== null) {
          var a = i.next;
          i.next = o, r.next = a;
        }
        t.pending = r;
      }
      ft = null;
    }
    return e;
  }
  function tc(e, n) {
    do {
      var t = Se;
      try {
        if (ti(), Cl.current = Pl, El) {
          for (var r = fe.memoizedState; r !== null; ) {
            var o = r.queue;
            o !== null && (o.pending = null), r = r.next;
          }
          El = !1;
        }
        if (pt = 0, ze = _e = fe = null, Er = !1, _r = 0, Oi.current = null, t === null || t.return === null) {
          xe = 1, Mr = n, Se = null;
          break;
        }
        e: {
          var i = e, a = t.return, d = t, p = n;
          if (n = De, d.flags |= 32768, p !== null && typeof p == "object" && typeof p.then == "function") {
            var w = p, x = d, P = x.tag;
            if ((x.mode & 1) === 0 && (P === 0 || P === 11 || P === 15)) {
              var C = x.alternate;
              C ? (x.updateQueue = C.updateQueue, x.memoizedState = C.memoizedState, x.lanes = C.lanes) : (x.updateQueue = null, x.memoizedState = null);
            }
            var L = Na(a);
            if (L !== null) {
              L.flags &= -257, za(L, a, d, i, n), L.mode & 1 && Pa(i, w, n), n = L, p = w;
              var I = n.updateQueue;
              if (I === null) {
                var F = /* @__PURE__ */ new Set();
                F.add(p), n.updateQueue = F;
              } else I.add(p);
              break e;
            } else {
              if ((n & 1) === 0) {
                Pa(i, w, n), Vi();
                break e;
              }
              p = Error(s(426));
            }
          } else if (ae && d.mode & 1) {
            var ye = Na(a);
            if (ye !== null) {
              (ye.flags & 65536) === 0 && (ye.flags |= 256), za(ye, a, d, i, n), ei(Vt(p, d));
              break e;
            }
          }
          i = p = Vt(p, d), xe !== 4 && (xe = 2), Tr === null ? Tr = [i] : Tr.push(i), i = a;
          do {
            switch (i.tag) {
              case 3:
                i.flags |= 65536, n &= -n, i.lanes |= n;
                var g = _a(i, p, n);
                Zs(i, g);
                break e;
              case 1:
                d = p;
                var h = i.type, y = i.stateNode;
                if ((i.flags & 128) === 0 && (typeof h.getDerivedStateFromError == "function" || y !== null && typeof y.componentDidCatch == "function" && (Zn === null || !Zn.has(y)))) {
                  i.flags |= 65536, n &= -n, i.lanes |= n;
                  var N = xa(i, d, n);
                  Zs(i, N);
                  break e;
                }
            }
            i = i.return;
          } while (i !== null);
        }
        oc(t);
      } catch (A) {
        n = A, Se === t && t !== null && (Se = t = t.return);
        continue;
      }
      break;
    } while (!0);
  }
  function rc() {
    var e = Rl.current;
    return Rl.current = Pl, e === null ? Pl : e;
  }
  function Vi() {
    (xe === 0 || xe === 3 || xe === 2) && (xe = 4), Me === null || (ht & 268435455) === 0 && (Dl & 268435455) === 0 || et(Me, De);
  }
  function Ul(e, n) {
    var t = Z;
    Z |= 2;
    var r = rc();
    (Me !== e || De !== n) && (In = null, vt(e, n));
    do
      try {
        Kd();
        break;
      } catch (o) {
        tc(e, o);
      }
    while (!0);
    if (ti(), Z = t, Rl.current = r, Se !== null) throw Error(s(261));
    return Me = null, De = 0, xe;
  }
  function Kd() {
    for (; Se !== null; ) lc(Se);
  }
  function Yd() {
    for (; Se !== null && !yf(); ) lc(Se);
  }
  function lc(e) {
    var n = sc(e.alternate, e, rn);
    e.memoizedProps = e.pendingProps, n === null ? oc(e) : Se = n, Oi.current = null;
  }
  function oc(e) {
    var n = e;
    do {
      var t = n.alternate;
      if (e = n.return, (n.flags & 32768) === 0) {
        if (t = Ud(t, n, rn), t !== null) {
          Se = t;
          return;
        }
      } else {
        if (t = Wd(t, n), t !== null) {
          t.flags &= 32767, Se = t;
          return;
        }
        if (e !== null) e.flags |= 32768, e.subtreeFlags = 0, e.deletions = null;
        else {
          xe = 6, Se = null;
          return;
        }
      }
      if (n = n.sibling, n !== null) {
        Se = n;
        return;
      }
      Se = n = e;
    } while (n !== null);
    xe === 0 && (xe = 5);
  }
  function gt(e, n, t) {
    var r = te, o = an.transition;
    try {
      an.transition = null, te = 1, qd(e, n, t, r);
    } finally {
      an.transition = o, te = r;
    }
    return null;
  }
  function qd(e, n, t, r) {
    do
      Yt();
    while (Jn !== null);
    if ((Z & 6) !== 0) throw Error(s(327));
    t = e.finishedWork;
    var o = e.finishedLanes;
    if (t === null) return null;
    if (e.finishedWork = null, e.finishedLanes = 0, t === e.current) throw Error(s(177));
    e.callbackNode = null, e.callbackPriority = 0;
    var i = t.lanes | t.childLanes;
    if (zf(e, i), e === Me && (Se = Me = null, De = 0), (t.subtreeFlags & 2064) === 0 && (t.flags & 2064) === 0 || Il || (Il = !0, ac(Vr, function() {
      return Yt(), null;
    })), i = (t.flags & 15990) !== 0, (t.subtreeFlags & 15990) !== 0 || i) {
      i = an.transition, an.transition = null;
      var a = te;
      te = 1;
      var d = Z;
      Z |= 4, Oi.current = null, Bd(e, t), Xa(t, e), hd(Vo), Gr = !!Bo, Vo = Bo = null, e.current = t, Vd(t), wf(), Z = d, te = a, an.transition = i;
    } else e.current = t;
    if (Il && (Il = !1, Jn = e, Fl = o), i = e.pendingLanes, i === 0 && (Zn = null), Cf(t.stateNode), qe(e, ge()), n !== null) for (r = e.onRecoverableError, t = 0; t < n.length; t++) o = n[t], r(o.value, { componentStack: o.stack, digest: o.digest });
    if (Ol) throw Ol = !1, e = ji, ji = null, e;
    return (Fl & 1) !== 0 && e.tag !== 0 && Yt(), i = e.pendingLanes, (i & 1) !== 0 ? e === Ai ? Lr++ : (Lr = 0, Ai = e) : Lr = 0, Yn(), null;
  }
  function Yt() {
    if (Jn !== null) {
      var e = Yu(Fl), n = an.transition, t = te;
      try {
        if (an.transition = null, te = 16 > e ? 16 : e, Jn === null) var r = !1;
        else {
          if (e = Jn, Jn = null, Fl = 0, (Z & 6) !== 0) throw Error(s(331));
          var o = Z;
          for (Z |= 4, R = e.current; R !== null; ) {
            var i = R, a = i.child;
            if ((R.flags & 16) !== 0) {
              var d = i.deletions;
              if (d !== null) {
                for (var p = 0; p < d.length; p++) {
                  var w = d[p];
                  for (R = w; R !== null; ) {
                    var x = R;
                    switch (x.tag) {
                      case 0:
                      case 11:
                      case 15:
                        zr(8, x, i);
                    }
                    var P = x.child;
                    if (P !== null) P.return = x, R = P;
                    else for (; R !== null; ) {
                      x = R;
                      var C = x.sibling, L = x.return;
                      if ($a(x), x === w) {
                        R = null;
                        break;
                      }
                      if (C !== null) {
                        C.return = L, R = C;
                        break;
                      }
                      R = L;
                    }
                  }
                }
                var I = i.alternate;
                if (I !== null) {
                  var F = I.child;
                  if (F !== null) {
                    I.child = null;
                    do {
                      var ye = F.sibling;
                      F.sibling = null, F = ye;
                    } while (F !== null);
                  }
                }
                R = i;
              }
            }
            if ((i.subtreeFlags & 2064) !== 0 && a !== null) a.return = i, R = a;
            else e: for (; R !== null; ) {
              if (i = R, (i.flags & 2048) !== 0) switch (i.tag) {
                case 0:
                case 11:
                case 15:
                  zr(9, i, i.return);
              }
              var g = i.sibling;
              if (g !== null) {
                g.return = i.return, R = g;
                break e;
              }
              R = i.return;
            }
          }
          var h = e.current;
          for (R = h; R !== null; ) {
            a = R;
            var y = a.child;
            if ((a.subtreeFlags & 2064) !== 0 && y !== null) y.return = a, R = y;
            else e: for (a = h; R !== null; ) {
              if (d = R, (d.flags & 2048) !== 0) try {
                switch (d.tag) {
                  case 0:
                  case 11:
                  case 15:
                    Ll(9, d);
                }
              } catch (A) {
                me(d, d.return, A);
              }
              if (d === a) {
                R = null;
                break e;
              }
              var N = d.sibling;
              if (N !== null) {
                N.return = d.return, R = N;
                break e;
              }
              R = d.return;
            }
          }
          if (Z = o, Yn(), Cn && typeof Cn.onPostCommitFiberRoot == "function") try {
            Cn.onPostCommitFiberRoot($r, e);
          } catch {
          }
          r = !0;
        }
        return r;
      } finally {
        te = t, an.transition = n;
      }
    }
    return !1;
  }
  function ic(e, n, t) {
    n = Vt(t, n), n = _a(e, n, 1), e = Xn(e, n, 1), n = We(), e !== null && (nr(e, 1, n), qe(e, n));
  }
  function me(e, n, t) {
    if (e.tag === 3) ic(e, e, t);
    else for (; n !== null; ) {
      if (n.tag === 3) {
        ic(n, e, t);
        break;
      } else if (n.tag === 1) {
        var r = n.stateNode;
        if (typeof n.type.getDerivedStateFromError == "function" || typeof r.componentDidCatch == "function" && (Zn === null || !Zn.has(r))) {
          e = Vt(t, e), e = xa(n, e, 1), n = Xn(n, e, 1), e = We(), n !== null && (nr(n, 1, e), qe(n, e));
          break;
        }
      }
      n = n.return;
    }
  }
  function Xd(e, n, t) {
    var r = e.pingCache;
    r !== null && r.delete(n), n = We(), e.pingedLanes |= e.suspendedLanes & t, Me === e && (De & t) === t && (xe === 4 || xe === 3 && (De & 130023424) === De && 500 > ge() - Fi ? vt(e, 0) : Ii |= t), qe(e, n);
  }
  function uc(e, n) {
    n === 0 && ((e.mode & 1) === 0 ? n = 1 : (n = Kr, Kr <<= 1, (Kr & 130023424) === 0 && (Kr = 4194304)));
    var t = We();
    e = Rn(e, n), e !== null && (nr(e, n, t), qe(e, t));
  }
  function Gd(e) {
    var n = e.memoizedState, t = 0;
    n !== null && (t = n.retryLane), uc(e, t);
  }
  function Zd(e, n) {
    var t = 0;
    switch (e.tag) {
      case 13:
        var r = e.stateNode, o = e.memoizedState;
        o !== null && (t = o.retryLane);
        break;
      case 19:
        r = e.stateNode;
        break;
      default:
        throw Error(s(314));
    }
    r !== null && r.delete(n), uc(e, t);
  }
  var sc;
  sc = function(e, n, t) {
    if (e !== null) if (e.memoizedProps !== n.pendingProps || $e.current) Ke = !0;
    else {
      if ((e.lanes & t) === 0 && (n.flags & 128) === 0) return Ke = !1, Ad(e, n, t);
      Ke = (e.flags & 131072) !== 0;
    }
    else Ke = !1, ae && (n.flags & 1048576) !== 0 && Hs(n, hl, n.index);
    switch (n.lanes = 0, n.tag) {
      case 2:
        var r = n.type;
        Ml(e, n), e = n.pendingProps;
        var o = It(n, Oe.current);
        Ht(n, t), o = pi(null, n, r, e, o, t);
        var i = hi();
        return n.flags |= 1, typeof o == "object" && o !== null && typeof o.render == "function" && o.$$typeof === void 0 ? (n.tag = 1, n.memoizedState = null, n.updateQueue = null, Qe(r) ? (i = !0, fl(n)) : i = !1, n.memoizedState = o.state !== null && o.state !== void 0 ? o.state : null, ii(n), o.updater = Nl, n.stateNode = o, o._reactInternals = n, ki(n, r, e, t), n = _i(null, n, r, !0, i, t)) : (n.tag = 0, ae && i && Go(n), Ue(null, n, o, t), n = n.child), n;
      case 16:
        r = n.elementType;
        e: {
          switch (Ml(e, n), e = n.pendingProps, o = r._init, r = o(r._payload), n.type = r, o = n.tag = bd(r), e = gn(r, e), o) {
            case 0:
              n = Ei(null, n, r, e, t);
              break e;
            case 1:
              n = Oa(null, n, r, e, t);
              break e;
            case 11:
              n = Ma(null, n, r, e, t);
              break e;
            case 14:
              n = Ta(null, n, r, gn(r.type, e), t);
              break e;
          }
          throw Error(s(
            306,
            r,
            ""
          ));
        }
        return n;
      case 0:
        return r = n.type, o = n.pendingProps, o = n.elementType === r ? o : gn(r, o), Ei(e, n, r, o, t);
      case 1:
        return r = n.type, o = n.pendingProps, o = n.elementType === r ? o : gn(r, o), Oa(e, n, r, o, t);
      case 3:
        e: {
          if (Ia(n), e === null) throw Error(s(387));
          r = n.pendingProps, i = n.memoizedState, o = i.element, Gs(e, n), kl(n, r, null, t);
          var a = n.memoizedState;
          if (r = a.element, i.isDehydrated) if (i = { element: r, isDehydrated: !1, cache: a.cache, pendingSuspenseBoundaries: a.pendingSuspenseBoundaries, transitions: a.transitions }, n.updateQueue.baseState = i, n.memoizedState = i, n.flags & 256) {
            o = Vt(Error(s(423)), n), n = Fa(e, n, r, t, o);
            break e;
          } else if (r !== o) {
            o = Vt(Error(s(424)), n), n = Fa(e, n, r, t, o);
            break e;
          } else for (tn = $n(n.stateNode.containerInfo.firstChild), nn = n, ae = !0, vn = null, t = qs(n, null, r, t), n.child = t; t; ) t.flags = t.flags & -3 | 4096, t = t.sibling;
          else {
            if (At(), r === o) {
              n = On(e, n, t);
              break e;
            }
            Ue(e, n, r, t);
          }
          n = n.child;
        }
        return n;
      case 5:
        return bs(n), e === null && bo(n), r = n.type, o = n.pendingProps, i = e !== null ? e.memoizedProps : null, a = o.children, $o(r, o) ? a = null : i !== null && $o(r, i) && (n.flags |= 32), Da(e, n), Ue(e, n, a, t), n.child;
      case 6:
        return e === null && bo(n), null;
      case 13:
        return ja(e, n, t);
      case 4:
        return ui(n, n.stateNode.containerInfo), r = n.pendingProps, e === null ? n.child = Ut(n, null, r, t) : Ue(e, n, r, t), n.child;
      case 11:
        return r = n.type, o = n.pendingProps, o = n.elementType === r ? o : gn(r, o), Ma(e, n, r, o, t);
      case 7:
        return Ue(e, n, n.pendingProps, t), n.child;
      case 8:
        return Ue(e, n, n.pendingProps.children, t), n.child;
      case 12:
        return Ue(e, n, n.pendingProps.children, t), n.child;
      case 10:
        e: {
          if (r = n.type._context, o = n.pendingProps, i = n.memoizedProps, a = o.value, le(gl, r._currentValue), r._currentValue = a, i !== null) if (mn(i.value, a)) {
            if (i.children === o.children && !$e.current) {
              n = On(e, n, t);
              break e;
            }
          } else for (i = n.child, i !== null && (i.return = n); i !== null; ) {
            var d = i.dependencies;
            if (d !== null) {
              a = i.child;
              for (var p = d.firstContext; p !== null; ) {
                if (p.context === r) {
                  if (i.tag === 1) {
                    p = Dn(-1, t & -t), p.tag = 2;
                    var w = i.updateQueue;
                    if (w !== null) {
                      w = w.shared;
                      var x = w.pending;
                      x === null ? p.next = p : (p.next = x.next, x.next = p), w.pending = p;
                    }
                  }
                  i.lanes |= t, p = i.alternate, p !== null && (p.lanes |= t), li(
                    i.return,
                    t,
                    n
                  ), d.lanes |= t;
                  break;
                }
                p = p.next;
              }
            } else if (i.tag === 10) a = i.type === n.type ? null : i.child;
            else if (i.tag === 18) {
              if (a = i.return, a === null) throw Error(s(341));
              a.lanes |= t, d = a.alternate, d !== null && (d.lanes |= t), li(a, t, n), a = i.sibling;
            } else a = i.child;
            if (a !== null) a.return = i;
            else for (a = i; a !== null; ) {
              if (a === n) {
                a = null;
                break;
              }
              if (i = a.sibling, i !== null) {
                i.return = a.return, a = i;
                break;
              }
              a = a.return;
            }
            i = a;
          }
          Ue(e, n, o.children, t), n = n.child;
        }
        return n;
      case 9:
        return o = n.type, r = n.pendingProps.children, Ht(n, t), o = un(o), r = r(o), n.flags |= 1, Ue(e, n, r, t), n.child;
      case 14:
        return r = n.type, o = gn(r, n.pendingProps), o = gn(r.type, o), Ta(e, n, r, o, t);
      case 15:
        return La(e, n, n.type, n.pendingProps, t);
      case 17:
        return r = n.type, o = n.pendingProps, o = n.elementType === r ? o : gn(r, o), Ml(e, n), n.tag = 1, Qe(r) ? (e = !0, fl(n)) : e = !1, Ht(n, t), Ca(n, r, o), ki(n, r, o, t), _i(null, n, r, !0, e, t);
      case 19:
        return Ua(e, n, t);
      case 22:
        return Ra(e, n, t);
    }
    throw Error(s(156, n.tag));
  };
  function ac(e, n) {
    return Bu(e, n);
  }
  function Jd(e, n, t, r) {
    this.tag = e, this.key = t, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.ref = null, this.pendingProps = n, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = r, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
  }
  function cn(e, n, t, r) {
    return new Jd(e, n, t, r);
  }
  function $i(e) {
    return e = e.prototype, !(!e || !e.isReactComponent);
  }
  function bd(e) {
    if (typeof e == "function") return $i(e) ? 1 : 0;
    if (e != null) {
      if (e = e.$$typeof, e === Ae) return 11;
      if (e === Sn) return 14;
    }
    return 2;
  }
  function nt(e, n) {
    var t = e.alternate;
    return t === null ? (t = cn(e.tag, n, e.key, e.mode), t.elementType = e.elementType, t.type = e.type, t.stateNode = e.stateNode, t.alternate = e, e.alternate = t) : (t.pendingProps = n, t.type = e.type, t.flags = 0, t.subtreeFlags = 0, t.deletions = null), t.flags = e.flags & 14680064, t.childLanes = e.childLanes, t.lanes = e.lanes, t.child = e.child, t.memoizedProps = e.memoizedProps, t.memoizedState = e.memoizedState, t.updateQueue = e.updateQueue, n = e.dependencies, t.dependencies = n === null ? null : { lanes: n.lanes, firstContext: n.firstContext }, t.sibling = e.sibling, t.index = e.index, t.ref = e.ref, t;
  }
  function Wl(e, n, t, r, o, i) {
    var a = 2;
    if (r = e, typeof e == "function") $i(e) && (a = 1);
    else if (typeof e == "string") a = 5;
    else e: switch (e) {
      case Ee:
        return yt(t.children, o, i, n);
      case G:
        a = 8, o |= 8;
        break;
      case Be:
        return e = cn(12, t, n, o | 2), e.elementType = Be, e.lanes = i, e;
      case Je:
        return e = cn(13, t, n, o), e.elementType = Je, e.lanes = i, e;
      case pn:
        return e = cn(19, t, n, o), e.elementType = pn, e.lanes = i, e;
      case he:
        return Hl(t, o, i, n);
      default:
        if (typeof e == "object" && e !== null) switch (e.$$typeof) {
          case ke:
            a = 10;
            break e;
          case Ne:
            a = 9;
            break e;
          case Ae:
            a = 11;
            break e;
          case Sn:
            a = 14;
            break e;
          case Ve:
            a = 16, r = null;
            break e;
        }
        throw Error(s(130, e == null ? e : typeof e, ""));
    }
    return n = cn(a, t, n, o), n.elementType = e, n.type = r, n.lanes = i, n;
  }
  function yt(e, n, t, r) {
    return e = cn(7, e, r, n), e.lanes = t, e;
  }
  function Hl(e, n, t, r) {
    return e = cn(22, e, r, n), e.elementType = he, e.lanes = t, e.stateNode = { isHidden: !1 }, e;
  }
  function Qi(e, n, t) {
    return e = cn(6, e, null, n), e.lanes = t, e;
  }
  function Ki(e, n, t) {
    return n = cn(4, e.children !== null ? e.children : [], e.key, n), n.lanes = t, n.stateNode = { containerInfo: e.containerInfo, pendingChildren: null, implementation: e.implementation }, n;
  }
  function ep(e, n, t, r, o) {
    this.tag = n, this.containerInfo = e, this.finishedWork = this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.pendingContext = this.context = null, this.callbackPriority = 0, this.eventTimes = wo(0), this.expirationTimes = wo(-1), this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = wo(0), this.identifierPrefix = r, this.onRecoverableError = o, this.mutableSourceEagerHydrationData = null;
  }
  function Yi(e, n, t, r, o, i, a, d, p) {
    return e = new ep(e, n, t, d, p), n === 1 ? (n = 1, i === !0 && (n |= 8)) : n = 0, i = cn(3, null, null, n), e.current = i, i.stateNode = e, i.memoizedState = { element: r, isDehydrated: t, cache: null, transitions: null, pendingSuspenseBoundaries: null }, ii(i), e;
  }
  function np(e, n, t) {
    var r = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
    return { $$typeof: Ce, key: r == null ? null : "" + r, children: e, containerInfo: n, implementation: t };
  }
  function cc(e) {
    if (!e) return Kn;
    e = e._reactInternals;
    e: {
      if (it(e) !== e || e.tag !== 1) throw Error(s(170));
      var n = e;
      do {
        switch (n.tag) {
          case 3:
            n = n.stateNode.context;
            break e;
          case 1:
            if (Qe(n.type)) {
              n = n.stateNode.__reactInternalMemoizedMergedChildContext;
              break e;
            }
        }
        n = n.return;
      } while (n !== null);
      throw Error(s(171));
    }
    if (e.tag === 1) {
      var t = e.type;
      if (Qe(t)) return As(e, t, n);
    }
    return n;
  }
  function fc(e, n, t, r, o, i, a, d, p) {
    return e = Yi(t, r, !0, e, o, i, a, d, p), e.context = cc(null), t = e.current, r = We(), o = bn(t), i = Dn(r, o), i.callback = n ?? null, Xn(t, i, o), e.current.lanes = o, nr(e, o, r), qe(e, r), e;
  }
  function Bl(e, n, t, r) {
    var o = n.current, i = We(), a = bn(o);
    return t = cc(t), n.context === null ? n.context = t : n.pendingContext = t, n = Dn(i, a), n.payload = { element: e }, r = r === void 0 ? null : r, r !== null && (n.callback = r), e = Xn(o, n, a), e !== null && (kn(e, o, a, i), wl(e, o, a)), a;
  }
  function Vl(e) {
    return e = e.current, e.child ? (e.child.tag === 5, e.child.stateNode) : null;
  }
  function dc(e, n) {
    if (e = e.memoizedState, e !== null && e.dehydrated !== null) {
      var t = e.retryLane;
      e.retryLane = t !== 0 && t < n ? t : n;
    }
  }
  function qi(e, n) {
    dc(e, n), (e = e.alternate) && dc(e, n);
  }
  function tp() {
    return null;
  }
  var pc = typeof reportError == "function" ? reportError : function(e) {
    console.error(e);
  };
  function Xi(e) {
    this._internalRoot = e;
  }
  $l.prototype.render = Xi.prototype.render = function(e) {
    var n = this._internalRoot;
    if (n === null) throw Error(s(409));
    Bl(e, n, null, null);
  }, $l.prototype.unmount = Xi.prototype.unmount = function() {
    var e = this._internalRoot;
    if (e !== null) {
      this._internalRoot = null;
      var n = e.containerInfo;
      mt(function() {
        Bl(null, e, null, null);
      }), n[zn] = null;
    }
  };
  function $l(e) {
    this._internalRoot = e;
  }
  $l.prototype.unstable_scheduleHydration = function(e) {
    if (e) {
      var n = Gu();
      e = { blockedOn: null, target: e, priority: n };
      for (var t = 0; t < Hn.length && n !== 0 && n < Hn[t].priority; t++) ;
      Hn.splice(t, 0, e), t === 0 && bu(e);
    }
  };
  function Gi(e) {
    return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11);
  }
  function Ql(e) {
    return !(!e || e.nodeType !== 1 && e.nodeType !== 9 && e.nodeType !== 11 && (e.nodeType !== 8 || e.nodeValue !== " react-mount-point-unstable "));
  }
  function hc() {
  }
  function rp(e, n, t, r, o) {
    if (o) {
      if (typeof r == "function") {
        var i = r;
        r = function() {
          var w = Vl(a);
          i.call(w);
        };
      }
      var a = fc(n, r, e, 0, null, !1, !1, "", hc);
      return e._reactRootContainer = a, e[zn] = a.current, mr(e.nodeType === 8 ? e.parentNode : e), mt(), a;
    }
    for (; o = e.lastChild; ) e.removeChild(o);
    if (typeof r == "function") {
      var d = r;
      r = function() {
        var w = Vl(p);
        d.call(w);
      };
    }
    var p = Yi(e, 0, !1, null, null, !1, !1, "", hc);
    return e._reactRootContainer = p, e[zn] = p.current, mr(e.nodeType === 8 ? e.parentNode : e), mt(function() {
      Bl(n, p, t, r);
    }), p;
  }
  function Kl(e, n, t, r, o) {
    var i = t._reactRootContainer;
    if (i) {
      var a = i;
      if (typeof o == "function") {
        var d = o;
        o = function() {
          var p = Vl(a);
          d.call(p);
        };
      }
      Bl(n, a, e, o);
    } else a = rp(t, n, e, o, r);
    return Vl(a);
  }
  qu = function(e) {
    switch (e.tag) {
      case 3:
        var n = e.stateNode;
        if (n.current.memoizedState.isDehydrated) {
          var t = er(n.pendingLanes);
          t !== 0 && (ko(n, t | 1), qe(n, ge()), (Z & 6) === 0 && (Kt = ge() + 500, Yn()));
        }
        break;
      case 13:
        mt(function() {
          var r = Rn(e, 1);
          if (r !== null) {
            var o = We();
            kn(r, e, 1, o);
          }
        }), qi(e, 1);
    }
  }, So = function(e) {
    if (e.tag === 13) {
      var n = Rn(e, 134217728);
      if (n !== null) {
        var t = We();
        kn(n, e, 134217728, t);
      }
      qi(e, 134217728);
    }
  }, Xu = function(e) {
    if (e.tag === 13) {
      var n = bn(e), t = Rn(e, n);
      if (t !== null) {
        var r = We();
        kn(t, e, n, r);
      }
      qi(e, n);
    }
  }, Gu = function() {
    return te;
  }, Zu = function(e, n) {
    var t = te;
    try {
      return te = e, n();
    } finally {
      te = t;
    }
  }, po = function(e, n, t) {
    switch (n) {
      case "input":
        if (lo(e, t), n = t.name, t.type === "radio" && n != null) {
          for (t = e; t.parentNode; ) t = t.parentNode;
          for (t = t.querySelectorAll("input[name=" + JSON.stringify("" + n) + '][type="radio"]'), n = 0; n < t.length; n++) {
            var r = t[n];
            if (r !== e && r.form === e.form) {
              var o = al(r);
              if (!o) throw Error(s(90));
              Su(r), lo(r, o);
            }
          }
        }
        break;
      case "textarea":
        Pu(e, t);
        break;
      case "select":
        n = t.value, n != null && Et(e, !!t.multiple, n, !1);
    }
  }, Iu = Hi, Fu = mt;
  var lp = { usingClientEntryPoint: !1, Events: [yr, Dt, al, Du, Ou, Hi] }, Rr = { findFiberByHostInstance: ut, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" }, op = { bundleType: Rr.bundleType, version: Rr.version, rendererPackageName: Rr.rendererPackageName, rendererConfig: Rr.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: we.ReactCurrentDispatcher, findHostInstanceByFiber: function(e) {
    return e = Wu(e), e === null ? null : e.stateNode;
  }, findFiberByHostInstance: Rr.findFiberByHostInstance || tp, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
    var Yl = __REACT_DEVTOOLS_GLOBAL_HOOK__;
    if (!Yl.isDisabled && Yl.supportsFiber) try {
      $r = Yl.inject(op), Cn = Yl;
    } catch {
    }
  }
  return Xe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = lp, Xe.createPortal = function(e, n) {
    var t = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
    if (!Gi(n)) throw Error(s(200));
    return np(e, n, null, t);
  }, Xe.createRoot = function(e, n) {
    if (!Gi(e)) throw Error(s(299));
    var t = !1, r = "", o = pc;
    return n != null && (n.unstable_strictMode === !0 && (t = !0), n.identifierPrefix !== void 0 && (r = n.identifierPrefix), n.onRecoverableError !== void 0 && (o = n.onRecoverableError)), n = Yi(e, 1, !1, null, null, t, !1, r, o), e[zn] = n.current, mr(e.nodeType === 8 ? e.parentNode : e), new Xi(n);
  }, Xe.findDOMNode = function(e) {
    if (e == null) return null;
    if (e.nodeType === 1) return e;
    var n = e._reactInternals;
    if (n === void 0)
      throw typeof e.render == "function" ? Error(s(188)) : (e = Object.keys(e).join(","), Error(s(268, e)));
    return e = Wu(n), e = e === null ? null : e.stateNode, e;
  }, Xe.flushSync = function(e) {
    return mt(e);
  }, Xe.hydrate = function(e, n, t) {
    if (!Ql(n)) throw Error(s(200));
    return Kl(null, e, n, !0, t);
  }, Xe.hydrateRoot = function(e, n, t) {
    if (!Gi(e)) throw Error(s(405));
    var r = t != null && t.hydratedSources || null, o = !1, i = "", a = pc;
    if (t != null && (t.unstable_strictMode === !0 && (o = !0), t.identifierPrefix !== void 0 && (i = t.identifierPrefix), t.onRecoverableError !== void 0 && (a = t.onRecoverableError)), n = fc(n, null, e, 1, t ?? null, o, !1, i, a), e[zn] = n.current, mr(e), r) for (e = 0; e < r.length; e++) t = r[e], o = t._getVersion, o = o(t._source), n.mutableSourceEagerHydrationData == null ? n.mutableSourceEagerHydrationData = [t, o] : n.mutableSourceEagerHydrationData.push(
      t,
      o
    );
    return new $l(n);
  }, Xe.render = function(e, n, t) {
    if (!Ql(n)) throw Error(s(200));
    return Kl(null, e, n, !1, t);
  }, Xe.unmountComponentAtNode = function(e) {
    if (!Ql(e)) throw Error(s(40));
    return e._reactRootContainer ? (mt(function() {
      Kl(null, null, e, !1, function() {
        e._reactRootContainer = null, e[zn] = null;
      });
    }), !0) : !1;
  }, Xe.unstable_batchedUpdates = Hi, Xe.unstable_renderSubtreeIntoContainer = function(e, n, t, r) {
    if (!Ql(t)) throw Error(s(200));
    if (e == null || e._reactInternals === void 0) throw Error(s(38));
    return Kl(e, n, t, !1, r);
  }, Xe.version = "18.3.1-next-f1338f8080-20240426", Xe;
}
var Cc;
function pp() {
  if (Cc) return bi.exports;
  Cc = 1;
  function l() {
    if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
      try {
        __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(l);
      } catch (u) {
        console.error(u);
      }
  }
  return l(), bi.exports = dp(), bi.exports;
}
var Ec;
function hp() {
  if (Ec) return ql;
  Ec = 1;
  var l = pp();
  return ql.createRoot = l.createRoot, ql.hydrateRoot = l.hydrateRoot, ql;
}
var mp = hp();
const vp = ["white", "black"], Zl = ["a", "b", "c", "d", "e", "f", "g", "h"], Jl = ["1", "2", "3", "4", "5", "6", "7", "8"], gp = [...Jl].reverse(), du = Array.prototype.concat(...Zl.map((l) => Jl.map((u) => l + u))), fn = (l) => du[8 * l[0] + l[1]], de = (l) => [l.charCodeAt(0) - 97, l.charCodeAt(1) - 49], Oc = du.map(de);
function yp(l) {
  let u;
  const s = () => (u === void 0 && (u = l()), u);
  return s.clear = () => {
    u = void 0;
  }, s;
}
const wp = () => {
  let l;
  return {
    start() {
      l = performance.now();
    },
    cancel() {
      l = void 0;
    },
    stop() {
      if (!l)
        return 0;
      const u = performance.now() - l;
      return l = void 0, u;
    }
  };
}, pu = (l) => l === "white" ? "black" : "white", Fr = (l, u) => {
  const s = l[0] - u[0], c = l[1] - u[1];
  return s * s + c * c;
}, uu = (l, u) => l.role === u.role && l.color === u.color, jr = (l) => (u, s) => [
  (s ? u[0] : 7 - u[0]) * l.width / 8,
  (s ? 7 - u[1] : u[1]) * l.height / 8
], Nn = (l, u) => {
  l.style.transform = `translate(${u[0]}px,${u[1]}px)`;
}, Ic = (l, u, s = 1) => {
  l.style.transform = `translate(${u[0]}px,${u[1]}px) scale(${s})`;
}, hu = (l, u) => {
  l.style.visibility = u ? "visible" : "hidden";
}, St = (l) => {
  var u;
  if (l.clientX || l.clientX === 0)
    return [l.clientX, l.clientY];
  if (!((u = l.targetTouches) === null || u === void 0) && u[0])
    return [l.targetTouches[0].clientX, l.targetTouches[0].clientY];
}, Fc = (l) => l.button === 2, jn = (l, u) => {
  const s = document.createElement(l);
  return u && (s.className = u), s;
};
function jc(l, u, s) {
  const c = de(l);
  return u || (c[0] = 7 - c[0], c[1] = 7 - c[1]), [
    s.left + s.width * c[0] / 8 + s.width / 16,
    s.top + s.height * (7 - c[1]) / 8 + s.height / 16
  ];
}
const kt = (l, u) => Math.abs(l - u), kp = (l) => (u, s, c, f) => kt(u, c) < 2 && (l === "white" ? (
  // allow 2 squares from first two ranks, for horde
  f === s + 1 || s <= 1 && f === s + 2 && u === c
) : f === s - 1 || s >= 6 && f === s - 2 && u === c), Ac = (l, u, s, c) => {
  const f = kt(l, s), m = kt(u, c);
  return f === 1 && m === 2 || f === 2 && m === 1;
}, Uc = (l, u, s, c) => kt(l, s) === kt(u, c), Wc = (l, u, s, c) => l === s || u === c, Hc = (l, u, s, c) => Uc(l, u, s, c) || Wc(l, u, s, c), Sp = (l, u, s) => (c, f, m, k) => kt(c, m) < 2 && kt(f, k) < 2 || s && f === k && f === (l === "white" ? 0 : 7) && (c === 4 && (m === 2 && u.includes(0) || m === 6 && u.includes(7)) || u.includes(m));
function Cp(l, u) {
  const s = u === "white" ? "1" : "8", c = [];
  for (const [f, m] of l)
    f[1] === s && m.color === u && m.role === "rook" && c.push(de(f)[0]);
  return c;
}
function Bc(l, u, s) {
  const c = l.get(u);
  if (!c)
    return [];
  const f = de(u), m = c.role, k = m === "pawn" ? kp(c.color) : m === "knight" ? Ac : m === "bishop" ? Uc : m === "rook" ? Wc : m === "queen" ? Hc : Sp(c.color, Cp(l, c.color), s);
  return Oc.filter((E) => (f[0] !== E[0] || f[1] !== E[1]) && k(f[0], f[1], E[0], E[1])).map(fn);
}
function Ge(l, ...u) {
  l && setTimeout(() => l(...u), 1);
}
function Ep(l) {
  l.orientation = pu(l.orientation), l.animation.current = l.draggable.current = l.selected = void 0;
}
function _p(l, u) {
  for (const [s, c] of u)
    c ? l.pieces.set(s, c) : l.pieces.delete(s);
}
function xp(l, u) {
  if (l.check = void 0, u === !0 && (u = l.turnColor), u)
    for (const [s, c] of l.pieces)
      c.role === "king" && c.color === u && (l.check = s);
}
function Pp(l, u, s, c) {
  ot(l), l.premovable.current = [u, s], Ge(l.premovable.events.set, u, s, c);
}
function lt(l) {
  l.premovable.current && (l.premovable.current = void 0, Ge(l.premovable.events.unset));
}
function Np(l, u, s) {
  lt(l), l.predroppable.current = { role: u, key: s }, Ge(l.predroppable.events.set, u, s);
}
function ot(l) {
  const u = l.predroppable;
  u.current && (u.current = void 0, Ge(u.events.unset));
}
function zp(l, u, s) {
  if (!l.autoCastle)
    return !1;
  const c = l.pieces.get(u);
  if (!c || c.role !== "king")
    return !1;
  const f = de(u), m = de(s);
  if (f[1] !== 0 && f[1] !== 7 || f[1] !== m[1])
    return !1;
  f[0] === 4 && !l.pieces.has(s) && (m[0] === 6 ? s = fn([7, m[1]]) : m[0] === 2 && (s = fn([0, m[1]])));
  const k = l.pieces.get(s);
  return !k || k.color !== c.color || k.role !== "rook" ? !1 : (l.pieces.delete(u), l.pieces.delete(s), f[0] < m[0] ? (l.pieces.set(fn([6, m[1]]), c), l.pieces.set(fn([5, m[1]]), k)) : (l.pieces.set(fn([2, m[1]]), c), l.pieces.set(fn([3, m[1]]), k)), !0);
}
function Vc(l, u, s) {
  const c = l.pieces.get(u), f = l.pieces.get(s);
  if (u === s || !c)
    return !1;
  const m = f && f.color !== c.color ? f : void 0;
  return s === l.selected && dn(l), Ge(l.events.move, u, s, m), zp(l, u, s) || (l.pieces.set(s, c), l.pieces.delete(u)), l.lastMove = [u, s], l.check = void 0, Ge(l.events.change), m || !0;
}
function mu(l, u, s, c) {
  if (l.pieces.has(s))
    if (c)
      l.pieces.delete(s);
    else
      return !1;
  return Ge(l.events.dropNewPiece, u, s), l.pieces.set(s, u), l.lastMove = [s], l.check = void 0, Ge(l.events.change), l.movable.dests = void 0, l.turnColor = pu(l.turnColor), !0;
}
function $c(l, u, s) {
  const c = Vc(l, u, s);
  return c && (l.movable.dests = void 0, l.turnColor = pu(l.turnColor), l.animation.current = void 0), c;
}
function Qc(l, u, s) {
  if (vu(l, u, s)) {
    const c = $c(l, u, s);
    if (c) {
      const f = l.hold.stop();
      dn(l);
      const m = {
        premove: !1,
        ctrlKey: l.stats.ctrlKey,
        holdTime: f
      };
      return c !== !0 && (m.captured = c), Ge(l.movable.events.after, u, s, m), !0;
    }
  } else if (Tp(l, u, s))
    return Pp(l, u, s, {
      ctrlKey: l.stats.ctrlKey
    }), dn(l), !0;
  return dn(l), !1;
}
function Kc(l, u, s, c) {
  const f = l.pieces.get(u);
  f && (Mp(l, u, s) || c) ? (l.pieces.delete(u), mu(l, f, s, c), Ge(l.movable.events.afterNewPiece, f.role, s, {
    premove: !1,
    predrop: !1
  })) : f && Lp(l, u, s) ? Np(l, f.role, s) : (lt(l), ot(l)), l.pieces.delete(u), dn(l);
}
function su(l, u, s) {
  if (Ge(l.events.select, u), l.selected) {
    if (l.selected === u && !l.draggable.enabled) {
      dn(l), l.hold.cancel();
      return;
    } else if ((l.selectable.enabled || s) && l.selected !== u && Qc(l, l.selected, u)) {
      l.stats.dragged = !1;
      return;
    }
  }
  (l.selectable.enabled || l.draggable.enabled) && (qc(l, u) || gu(l, u)) && (Yc(l, u), l.hold.start());
}
function Yc(l, u) {
  l.selected = u, gu(l, u) ? l.premovable.customDests || (l.premovable.dests = Bc(l.pieces, u, l.premovable.castle)) : l.premovable.dests = void 0;
}
function dn(l) {
  l.selected = void 0, l.premovable.dests = void 0, l.hold.cancel();
}
function qc(l, u) {
  const s = l.pieces.get(u);
  return !!s && (l.movable.color === "both" || l.movable.color === s.color && l.turnColor === s.color);
}
const vu = (l, u, s) => {
  var c, f;
  return u !== s && qc(l, u) && (l.movable.free || !!(!((f = (c = l.movable.dests) === null || c === void 0 ? void 0 : c.get(u)) === null || f === void 0) && f.includes(s)));
};
function Mp(l, u, s) {
  const c = l.pieces.get(u);
  return !!c && (u === s || !l.pieces.has(s)) && (l.movable.color === "both" || l.movable.color === c.color && l.turnColor === c.color);
}
function gu(l, u) {
  const s = l.pieces.get(u);
  return !!s && l.premovable.enabled && l.movable.color === s.color && l.turnColor !== s.color;
}
function Tp(l, u, s) {
  var c, f;
  const m = (f = (c = l.premovable.customDests) === null || c === void 0 ? void 0 : c.get(u)) !== null && f !== void 0 ? f : Bc(l.pieces, u, l.premovable.castle);
  return u !== s && gu(l, u) && m.includes(s);
}
function Lp(l, u, s) {
  const c = l.pieces.get(u), f = l.pieces.get(s);
  return !!c && (!f || f.color !== l.movable.color) && l.predroppable.enabled && (c.role !== "pawn" || s[1] !== "1" && s[1] !== "8") && l.movable.color === c.color && l.turnColor !== c.color;
}
function Rp(l, u) {
  const s = l.pieces.get(u);
  return !!s && l.draggable.enabled && (l.movable.color === "both" || l.movable.color === s.color && (l.turnColor === s.color || l.premovable.enabled));
}
function Dp(l) {
  const u = l.premovable.current;
  if (!u)
    return !1;
  const s = u[0], c = u[1];
  let f = !1;
  if (vu(l, s, c)) {
    const m = $c(l, s, c);
    if (m) {
      const k = { premove: !0 };
      m !== !0 && (k.captured = m), Ge(l.movable.events.after, s, c, k), f = !0;
    }
  }
  return lt(l), f;
}
function Op(l, u) {
  const s = l.predroppable.current;
  let c = !1;
  if (!s)
    return !1;
  if (u(s)) {
    const f = {
      role: s.role,
      color: l.movable.color
    };
    mu(l, f, s.key) && (Ge(l.movable.events.afterNewPiece, s.role, s.key, {
      premove: !1,
      predrop: !0
    }), c = !0);
  }
  return ot(l), c;
}
function yu(l) {
  lt(l), ot(l), dn(l);
}
function _c(l) {
  l.movable.color = l.movable.dests = l.animation.current = void 0, yu(l);
}
function Ct(l, u, s) {
  let c = Math.floor(8 * (l[0] - s.left) / s.width);
  u || (c = 7 - c);
  let f = 7 - Math.floor(8 * (l[1] - s.top) / s.height);
  return u || (f = 7 - f), c >= 0 && c < 8 && f >= 0 && f < 8 ? fn([c, f]) : void 0;
}
function Ip(l, u, s, c) {
  const f = de(l), m = Oc.filter((S) => Hc(f[0], f[1], S[0], S[1]) || Ac(f[0], f[1], S[0], S[1])), E = m.map((S) => jc(fn(S), s, c)).map((S) => Fr(u, S)), [, z] = E.reduce((S, j, M) => S[0] < j ? S : [j, M], [E[0], 0]);
  return fn(m[z]);
}
const Ze = (l) => l.orientation === "white", Xc = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", Fp = {
  p: "pawn",
  r: "rook",
  n: "knight",
  b: "bishop",
  q: "queen",
  k: "king"
}, jp = {
  pawn: "p",
  rook: "r",
  knight: "n",
  bishop: "b",
  queen: "q",
  king: "k"
};
function Gc(l) {
  l === "start" && (l = Xc);
  const u = /* @__PURE__ */ new Map();
  let s = 7, c = 0;
  for (const f of l)
    switch (f) {
      case " ":
      case "[":
        return u;
      case "/":
        if (--s, s < 0)
          return u;
        c = 0;
        break;
      case "~": {
        const m = u.get(fn([c - 1, s]));
        m && (m.promoted = !0);
        break;
      }
      default: {
        const m = f.charCodeAt(0);
        if (m < 57)
          c += m - 48;
        else {
          const k = f.toLowerCase();
          u.set(fn([c, s]), {
            role: Fp[k],
            color: f === k ? "black" : "white"
          }), ++c;
        }
      }
    }
  return u;
}
function Ap(l) {
  return gp.map((u) => Zl.map((s) => {
    const c = l.get(s + u);
    if (c) {
      let f = jp[c.role];
      return c.color === "white" && (f = f.toUpperCase()), c.promoted && (f += "~"), f;
    } else
      return "1";
  }).join("")).join("/").replace(/1{2,}/g, (u) => u.length.toString());
}
function Zc(l, u) {
  u.animation && (wu(l.animation, u.animation), (l.animation.duration || 0) < 70 && (l.animation.enabled = !1));
}
function Jc(l, u) {
  var s, c, f;
  if (!((s = u.movable) === null || s === void 0) && s.dests && (l.movable.dests = void 0), !((c = u.drawable) === null || c === void 0) && c.autoShapes && (l.drawable.autoShapes = []), wu(l, u), u.fen && (l.pieces = Gc(u.fen), l.drawable.shapes = ((f = u.drawable) === null || f === void 0 ? void 0 : f.shapes) || []), "check" in u && xp(l, u.check || !1), "lastMove" in u && !u.lastMove ? l.lastMove = void 0 : u.lastMove && (l.lastMove = u.lastMove), l.selected && Yc(l, l.selected), Zc(l, u), !l.movable.rookCastle && l.movable.dests) {
    const m = l.movable.color === "white" ? "1" : "8", k = "e" + m, E = l.movable.dests.get(k), z = l.pieces.get(k);
    if (!E || !z || z.role !== "king")
      return;
    l.movable.dests.set(k, E.filter((S) => !(S === "a" + m && E.includes("c" + m)) && !(S === "h" + m && E.includes("g" + m))));
  }
}
function wu(l, u) {
  for (const s in u)
    s === "__proto__" || s === "constructor" || !Object.prototype.hasOwnProperty.call(u, s) || (Object.prototype.hasOwnProperty.call(l, s) && xc(l[s]) && xc(u[s]) ? wu(l[s], u[s]) : l[s] = u[s]);
}
function xc(l) {
  if (typeof l != "object" || l === null)
    return !1;
  const u = Object.getPrototypeOf(l);
  return u === Object.prototype || u === null;
}
const wt = (l, u) => u.animation.enabled ? Hp(l, u) : rt(l, u);
function rt(l, u) {
  const s = l(u);
  return u.dom.redraw(), s;
}
const tu = (l, u) => ({
  key: l,
  pos: de(l),
  piece: u
}), Up = (l, u) => u.sort((s, c) => Fr(l.pos, s.pos) - Fr(l.pos, c.pos))[0];
function Wp(l, u) {
  const s = /* @__PURE__ */ new Map(), c = [], f = /* @__PURE__ */ new Map(), m = [], k = [], E = /* @__PURE__ */ new Map();
  let z, S, j;
  for (const [M, B] of l)
    E.set(M, tu(M, B));
  for (const M of du)
    z = u.pieces.get(M), S = E.get(M), z ? S ? uu(z, S.piece) || (m.push(S), k.push(tu(M, z))) : k.push(tu(M, z)) : S && m.push(S);
  for (const M of k)
    S = Up(M, m.filter((B) => uu(M.piece, B.piece))), S && (j = [S.pos[0] - M.pos[0], S.pos[1] - M.pos[1]], s.set(M.key, j.concat(j)), c.push(S.key));
  for (const M of m)
    c.includes(M.key) || f.set(M.key, M.piece);
  return {
    anims: s,
    fadings: f
  };
}
function bc(l, u) {
  const s = l.animation.current;
  if (s === void 0) {
    l.dom.destroyed || l.dom.redrawNow();
    return;
  }
  const c = 1 - (u - s.start) * s.frequency;
  if (c <= 0)
    l.animation.current = void 0, l.dom.redrawNow();
  else {
    const f = Bp(c);
    for (const m of s.plan.anims.values())
      m[2] = m[0] * f, m[3] = m[1] * f;
    l.dom.redrawNow(!0), requestAnimationFrame((m = performance.now()) => bc(l, m));
  }
}
function Hp(l, u) {
  const s = new Map(u.pieces), c = l(u), f = Wp(s, u);
  if (f.anims.size || f.fadings.size) {
    const m = u.animation.current && u.animation.current.start;
    u.animation.current = {
      start: performance.now(),
      frequency: 1 / u.animation.duration,
      plan: f
    }, m || bc(u, performance.now());
  } else
    u.dom.redraw();
  return c;
}
const Bp = (l) => l < 0.5 ? 4 * l * l * l : (l - 1) * (2 * l - 2) * (2 * l - 2) + 1, Vp = ["green", "red", "blue", "yellow"];
function $p(l, u) {
  if (u.touches && u.touches.length > 1)
    return;
  u.stopPropagation(), u.preventDefault(), u.ctrlKey ? dn(l) : yu(l);
  const s = St(u), c = Ct(s, Ze(l), l.dom.bounds());
  c && (l.drawable.current = {
    orig: c,
    pos: s,
    brush: qp(u),
    snapToValidMove: l.drawable.defaultSnapToValidMove
  }, ef(l));
}
function ef(l) {
  requestAnimationFrame(() => {
    const u = l.drawable.current;
    if (u) {
      const s = Ct(u.pos, Ze(l), l.dom.bounds());
      s || (u.snapToValidMove = !1);
      const c = u.snapToValidMove ? Ip(u.orig, u.pos, Ze(l), l.dom.bounds()) : s;
      c !== u.mouseSq && (u.mouseSq = c, u.dest = c !== u.orig ? c : void 0, l.dom.redrawNow()), ef(l);
    }
  });
}
function Qp(l, u) {
  l.drawable.current && (l.drawable.current.pos = St(u));
}
function Kp(l) {
  const u = l.drawable.current;
  u && (u.mouseSq && Xp(l.drawable, u), nf(l));
}
function nf(l) {
  l.drawable.current && (l.drawable.current = void 0, l.dom.redraw());
}
function Yp(l) {
  l.drawable.shapes.length && (l.drawable.shapes = [], l.dom.redraw(), tf(l.drawable));
}
function qp(l) {
  var u;
  const s = (l.shiftKey || l.ctrlKey) && Fc(l), c = l.altKey || l.metaKey || ((u = l.getModifierState) === null || u === void 0 ? void 0 : u.call(l, "AltGraph"));
  return Vp[(s ? 1 : 0) + (c ? 2 : 0)];
}
function Xp(l, u) {
  const s = (f) => f.orig === u.orig && f.dest === u.dest, c = l.shapes.find(s);
  c && (l.shapes = l.shapes.filter((f) => !s(f))), (!c || c.brush !== u.brush) && l.shapes.push({
    orig: u.orig,
    dest: u.dest,
    brush: u.brush
  }), tf(l);
}
function tf(l) {
  l.onChange && l.onChange(l.shapes);
}
function Gp(l, u) {
  if (!(l.trustAllEvents || u.isTrusted) || u.buttons !== void 0 && u.buttons > 1 || u.touches && u.touches.length > 1)
    return;
  const s = l.dom.bounds(), c = St(u), f = Ct(c, Ze(l), s);
  if (!f)
    return;
  const m = l.pieces.get(f), k = l.selected;
  if (!k && l.drawable.enabled && (l.drawable.eraseOnClick || !m || m.color !== l.turnColor) && Yp(l), u.cancelable !== !1 && (!u.touches || l.blockTouchScroll || m || k || Zp(l, c)))
    u.preventDefault();
  else if (u.touches)
    return;
  const E = !!l.premovable.current, z = !!l.predroppable.current;
  l.stats.ctrlKey = u.ctrlKey, l.selected && vu(l, l.selected, f) ? wt((M) => su(M, f), l) : su(l, f);
  const S = l.selected === f, j = lf(l, f);
  if (m && j && S && Rp(l, f)) {
    l.draggable.current = {
      orig: f,
      piece: m,
      origPos: c,
      pos: c,
      started: l.draggable.autoDistance && l.stats.dragged,
      element: j,
      previouslySelected: k,
      originTarget: u.target,
      keyHasChanged: !1
    }, j.cgDragging = !0, j.classList.add("dragging");
    const M = l.dom.elements.ghost;
    M && (M.className = `ghost ${m.color} ${m.role}`, Nn(M, jr(s)(de(f), Ze(l))), hu(M, !0)), ku(l);
  } else
    E && lt(l), z && ot(l);
  l.dom.redraw();
}
function Zp(l, u) {
  const s = Ze(l), c = l.dom.bounds(), f = Math.pow(c.width / 8, 2);
  for (const m of l.pieces.keys()) {
    const k = jc(m, s, c);
    if (Fr(k, u) <= f)
      return !0;
  }
  return !1;
}
function Jp(l, u, s, c) {
  l.pieces.set("a0", u), l.dom.redraw();
  const m = St(s);
  l.draggable.current = {
    orig: "a0",
    piece: u,
    origPos: m,
    pos: m,
    started: !0,
    element: () => lf(l, "a0"),
    originTarget: s.target,
    newPiece: !0,
    force: !!c,
    keyHasChanged: !1
  }, ku(l);
}
function ku(l) {
  requestAnimationFrame(() => {
    var u;
    const s = l.draggable.current;
    if (!s)
      return;
    !((u = l.animation.current) === null || u === void 0) && u.plan.anims.has(s.orig) && (l.animation.current = void 0);
    const c = l.pieces.get(s.orig);
    if (!c || !uu(c, s.piece))
      bl(l);
    else if (!s.started && Fr(s.pos, s.origPos) >= Math.pow(l.draggable.distance, 2) && (s.started = !0), s.started) {
      if (typeof s.element == "function") {
        const m = s.element();
        if (!m)
          return;
        m.cgDragging = !0, m.classList.add("dragging"), s.element = m;
      }
      const f = l.dom.bounds();
      Nn(s.element, [
        s.pos[0] - f.left - f.width / 16,
        s.pos[1] - f.top - f.height / 16
      ]), s.keyHasChanged || (s.keyHasChanged = s.orig !== Ct(s.pos, Ze(l), f));
    }
    ku(l);
  });
}
function bp(l, u) {
  l.draggable.current && (!u.touches || u.touches.length < 2) && (l.draggable.current.pos = St(u));
}
function eh(l, u) {
  const s = l.draggable.current;
  if (!s)
    return;
  if (u.type === "touchend" && u.cancelable !== !1 && u.preventDefault(), u.type === "touchend" && s.originTarget !== u.target && !s.newPiece) {
    l.draggable.current = void 0;
    return;
  }
  lt(l), ot(l);
  const c = St(u) || s.pos, f = Ct(c, Ze(l), l.dom.bounds());
  f && s.started && s.orig !== f ? s.newPiece ? Kc(l, s.orig, f, s.force) : (l.stats.ctrlKey = u.ctrlKey, Qc(l, s.orig, f) && (l.stats.dragged = !0)) : s.newPiece ? l.pieces.delete(s.orig) : l.draggable.deleteOnDropOff && !f && (l.pieces.delete(s.orig), Ge(l.events.change)), (s.orig === s.previouslySelected || s.keyHasChanged) && (s.orig === f || !f) ? dn(l) : l.selectable.enabled || dn(l), rf(l), l.draggable.current = void 0, l.dom.redraw();
}
function bl(l) {
  const u = l.draggable.current;
  u && (u.newPiece && l.pieces.delete(u.orig), l.draggable.current = void 0, dn(l), rf(l), l.dom.redraw());
}
function rf(l) {
  const u = l.dom.elements;
  u.ghost && hu(u.ghost, !1);
}
function lf(l, u) {
  let s = l.dom.elements.board.firstChild;
  for (; s; ) {
    if (s.cgKey === u && s.tagName === "PIECE")
      return s;
    s = s.nextSibling;
  }
}
function nh(l, u) {
  l.exploding = { stage: 1, keys: u }, l.dom.redraw(), setTimeout(() => {
    Pc(l, 2), setTimeout(() => Pc(l, void 0), 120);
  }, 120);
}
function Pc(l, u) {
  l.exploding && (u ? l.exploding.stage = u : l.exploding = void 0, l.dom.redraw());
}
function th(l, u) {
  function s() {
    Ep(l), u();
  }
  return {
    set(c) {
      c.orientation && c.orientation !== l.orientation && s(), Zc(l, c), (c.fen ? wt : rt)((f) => Jc(f, c), l);
    },
    state: l,
    getFen: () => Ap(l.pieces),
    toggleOrientation: s,
    setPieces(c) {
      wt((f) => _p(f, c), l);
    },
    selectSquare(c, f) {
      c ? wt((m) => su(m, c, f), l) : l.selected && (dn(l), l.dom.redraw());
    },
    move(c, f) {
      wt((m) => Vc(m, c, f), l);
    },
    newPiece(c, f) {
      wt((m) => mu(m, c, f), l);
    },
    playPremove() {
      if (l.premovable.current) {
        if (wt(Dp, l))
          return !0;
        l.dom.redraw();
      }
      return !1;
    },
    playPredrop(c) {
      if (l.predroppable.current) {
        const f = Op(l, c);
        return l.dom.redraw(), f;
      }
      return !1;
    },
    cancelPremove() {
      rt(lt, l);
    },
    cancelPredrop() {
      rt(ot, l);
    },
    cancelMove() {
      rt((c) => {
        yu(c), bl(c);
      }, l);
    },
    stop() {
      rt((c) => {
        _c(c), bl(c);
      }, l);
    },
    explode(c) {
      nh(l, c);
    },
    setAutoShapes(c) {
      rt((f) => f.drawable.autoShapes = c, l);
    },
    setShapes(c) {
      rt((f) => f.drawable.shapes = c, l);
    },
    getKeyAtDomPos(c) {
      return Ct(c, Ze(l), l.dom.bounds());
    },
    redrawAll: u,
    dragNewPiece(c, f, m) {
      Jp(l, c, f, m);
    },
    destroy() {
      _c(l), l.dom.unbind && l.dom.unbind(), l.dom.destroyed = !0;
    }
  };
}
function rh() {
  return {
    pieces: Gc(Xc),
    orientation: "white",
    turnColor: "white",
    coordinates: !0,
    coordinatesOnSquares: !1,
    ranksPosition: "right",
    autoCastle: !0,
    viewOnly: !1,
    disableContextMenu: !1,
    addPieceZIndex: !1,
    blockTouchScroll: !1,
    pieceKey: !1,
    trustAllEvents: !1,
    highlight: {
      lastMove: !0,
      check: !0
    },
    animation: {
      enabled: !0,
      duration: 200
    },
    movable: {
      free: !0,
      color: "both",
      showDests: !0,
      events: {},
      rookCastle: !0
    },
    premovable: {
      enabled: !0,
      showDests: !0,
      castle: !0,
      events: {}
    },
    predroppable: {
      enabled: !1,
      events: {}
    },
    draggable: {
      enabled: !0,
      distance: 3,
      autoDistance: !0,
      showGhost: !0,
      deleteOnDropOff: !1
    },
    dropmode: {
      active: !1
    },
    selectable: {
      enabled: !0
    },
    stats: {
      // on touchscreen, default to "tap-tap" moves
      // instead of drag
      dragged: !("ontouchstart" in window)
    },
    events: {},
    drawable: {
      enabled: !0,
      // can draw
      visible: !0,
      // can view
      defaultSnapToValidMove: !0,
      eraseOnClick: !0,
      shapes: [],
      autoShapes: [],
      brushes: {
        green: { key: "g", color: "#15781B", opacity: 1, lineWidth: 10 },
        red: { key: "r", color: "#882020", opacity: 1, lineWidth: 10 },
        blue: { key: "b", color: "#003088", opacity: 1, lineWidth: 10 },
        yellow: { key: "y", color: "#e68f00", opacity: 1, lineWidth: 10 },
        paleBlue: { key: "pb", color: "#003088", opacity: 0.4, lineWidth: 15 },
        paleGreen: { key: "pg", color: "#15781B", opacity: 0.4, lineWidth: 15 },
        paleRed: { key: "pr", color: "#882020", opacity: 0.4, lineWidth: 15 },
        paleGrey: {
          key: "pgr",
          color: "#4a4a4a",
          opacity: 0.35,
          lineWidth: 15
        },
        purple: { key: "purple", color: "#68217a", opacity: 0.65, lineWidth: 10 },
        pink: { key: "pink", color: "#ee2080", opacity: 0.5, lineWidth: 10 },
        white: { key: "white", color: "white", opacity: 1, lineWidth: 10 }
      },
      prevSvgHash: ""
    },
    hold: wp()
  };
}
const Nc = {
  hilitePrimary: { key: "hilitePrimary", color: "#3291ff", opacity: 1, lineWidth: 1 },
  hiliteWhite: { key: "hiliteWhite", color: "#ffffff", opacity: 1, lineWidth: 1 }
};
function lh() {
  const l = Pe("defs"), u = He(Pe("filter"), { id: "cg-filter-blur" });
  return u.appendChild(He(Pe("feGaussianBlur"), { stdDeviation: "0.019" })), l.appendChild(u), l;
}
function oh(l, u, s) {
  var c;
  const f = l.drawable, m = f.current, k = m && m.mouseSq ? m : void 0, E = /* @__PURE__ */ new Map(), z = l.dom.bounds(), S = f.autoShapes.filter(($) => !$.piece);
  for (const $ of f.shapes.concat(S).concat(k ? [k] : [])) {
    if (!$.dest)
      continue;
    const Q = (c = E.get($.dest)) !== null && c !== void 0 ? c : /* @__PURE__ */ new Set(), O = to(no(de($.orig), l.orientation), z), Y = to(no(de($.dest), l.orientation), z);
    Q.add(cu(O, Y)), E.set($.dest, Q);
  }
  const j = f.shapes.concat(S).map(($) => ({
    shape: $,
    current: !1,
    hash: zc($, au($.dest, E), !1, z)
  }));
  k && j.push({
    shape: k,
    current: !0,
    hash: zc(k, au(k.dest, E), !0, z)
  });
  const M = j.map(($) => $.hash).join(";");
  if (M === l.drawable.prevSvgHash)
    return;
  l.drawable.prevSvgHash = M;
  const B = u.querySelector("defs");
  ih(f, j, B), uh(j, u.querySelector("g"), s.querySelector("g"), ($) => ch(l, $, f.brushes, E, z));
}
function ih(l, u, s) {
  var c;
  const f = /* @__PURE__ */ new Map();
  let m;
  for (const z of u.filter((S) => S.shape.dest && S.shape.brush))
    m = of(l.brushes[z.shape.brush], z.shape.modifiers), !((c = z.shape.modifiers) === null || c === void 0) && c.hilite && f.set(eo(m).key, eo(m)), f.set(m.key, m);
  const k = /* @__PURE__ */ new Set();
  let E = s.firstElementChild;
  for (; E; )
    k.add(E.getAttribute("cgKey")), E = E.nextElementSibling;
  for (const [z, S] of f.entries())
    k.has(z) || s.appendChild(ph(S));
}
function uh(l, u, s, c) {
  const f = /* @__PURE__ */ new Map();
  for (const m of l)
    f.set(m.hash, !1);
  for (const m of [u, s]) {
    const k = [];
    let E = m.firstElementChild, z;
    for (; E; )
      z = E.getAttribute("cgHash"), f.has(z) ? f.set(z, !0) : k.push(E), E = E.nextElementSibling;
    for (const S of k)
      m.removeChild(S);
  }
  for (const m of l.filter((k) => !f.get(k.hash)))
    for (const k of c(m))
      k.isCustom ? s.appendChild(k.el) : u.appendChild(k.el);
}
function zc({ orig: l, dest: u, brush: s, piece: c, modifiers: f, customSvg: m, label: k }, E, z, S) {
  var j, M;
  return [
    S.width,
    S.height,
    z,
    l,
    u,
    s,
    E && "-",
    c && sh(c),
    f && ah(f),
    m && `custom-${Mc(m.html)},${(M = (j = m.center) === null || j === void 0 ? void 0 : j[0]) !== null && M !== void 0 ? M : "o"}`,
    k && `label-${Mc(k.text)}`
  ].filter((B) => B).join(",");
}
function sh(l) {
  return [l.color, l.role, l.scale].filter((u) => u).join(",");
}
function ah(l) {
  return [l.lineWidth, l.hilite && "*"].filter((u) => u).join(",");
}
function Mc(l) {
  let u = 0;
  for (let s = 0; s < l.length; s++)
    u = (u << 5) - u + l.charCodeAt(s) >>> 0;
  return u.toString();
}
function ch(l, { shape: u, current: s, hash: c }, f, m, k) {
  var E, z;
  const S = to(no(de(u.orig), l.orientation), k), j = u.dest ? to(no(de(u.dest), l.orientation), k) : S, M = u.brush && of(f[u.brush], u.modifiers), B = m.get(u.dest), $ = [];
  if (M) {
    const Q = He(Pe("g"), { cgHash: c });
    $.push({ el: Q }), S[0] !== j[0] || S[1] !== j[1] ? Q.appendChild(dh(u, M, S, j, s, au(u.dest, m))) : Q.appendChild(fh(f[u.brush], S, s, k));
  }
  if (u.label) {
    const Q = u.label;
    (E = Q.fill) !== null && E !== void 0 || (Q.fill = u.brush && f[u.brush].color);
    const O = u.brush ? void 0 : "tr";
    $.push({ el: hh(Q, c, S, j, B, O), isCustom: !0 });
  }
  if (u.customSvg) {
    const Q = (z = u.customSvg.center) !== null && z !== void 0 ? z : "orig", [O, Y] = Q === "label" ? sf(S, j, B).map((ue) => ue - 0.5) : Q === "dest" ? j : S, ve = He(Pe("g"), { transform: `translate(${O},${Y})`, cgHash: c });
    ve.innerHTML = `<svg width="1" height="1" viewBox="0 0 100 100">${u.customSvg.html}</svg>`, $.push({ el: ve, isCustom: !0 });
  }
  return $;
}
function fh(l, u, s, c) {
  const f = mh(), m = (c.width + c.height) / (4 * Math.max(c.width, c.height));
  return He(Pe("circle"), {
    stroke: l.color,
    "stroke-width": f[s ? 0 : 1],
    fill: "none",
    opacity: uf(l, s),
    cx: u[0],
    cy: u[1],
    r: m - f[1] / 2
  });
}
function eo(l) {
  return ["#ffffff", "#fff", "white"].includes(l.color) ? Nc.hilitePrimary : Nc.hiliteWhite;
}
function dh(l, u, s, c, f, m) {
  var k;
  function E(j) {
    var M;
    const B = gh(m && !f), $ = c[0] - s[0], Q = c[1] - s[1], O = Math.atan2(Q, $), Y = Math.cos(O) * B, ve = Math.sin(O) * B;
    return He(Pe("line"), {
      stroke: j ? eo(u).color : u.color,
      "stroke-width": vh(u, f) + (j ? 0.04 : 0),
      "stroke-linecap": "round",
      "marker-end": `url(#arrowhead-${j ? eo(u).key : u.key})`,
      opacity: !((M = l.modifiers) === null || M === void 0) && M.hilite ? 1 : uf(u, f),
      x1: s[0],
      y1: s[1],
      x2: c[0] - Y,
      y2: c[1] - ve
    });
  }
  if (!(!((k = l.modifiers) === null || k === void 0) && k.hilite))
    return E(!1);
  const z = Pe("g"), S = He(Pe("g"), { filter: "url(#cg-filter-blur)" });
  return S.appendChild(yh(s, c)), S.appendChild(E(!0)), z.appendChild(S), z.appendChild(E(!1)), z;
}
function ph(l) {
  const u = He(Pe("marker"), {
    id: "arrowhead-" + l.key,
    orient: "auto",
    overflow: "visible",
    markerWidth: 4,
    markerHeight: 4,
    refX: l.key.startsWith("hilite") ? 1.86 : 2.05,
    refY: 2
  });
  return u.appendChild(He(Pe("path"), {
    d: "M0,0 V4 L3,2 Z",
    fill: l.color
  })), u.setAttribute("cgKey", l.key), u;
}
function hh(l, u, s, c, f, m) {
  var k;
  const z = 0.4 * 0.75 ** l.text.length, S = sf(s, c, f), j = m === "tr" ? 0.4 : 0, M = He(Pe("g"), {
    transform: `translate(${S[0] + j},${S[1] - j})`,
    cgHash: u
  });
  M.appendChild(He(Pe("circle"), {
    r: 0.4 / 2,
    "fill-opacity": m ? 1 : 0.8,
    "stroke-opacity": m ? 1 : 0.7,
    "stroke-width": 0.03,
    fill: (k = l.fill) !== null && k !== void 0 ? k : "#666",
    stroke: "white"
  }));
  const B = He(Pe("text"), {
    "font-size": z,
    "font-family": "Noto Sans",
    "text-anchor": "middle",
    fill: "white",
    y: 0.13 * 0.75 ** l.text.length
  });
  return B.innerHTML = l.text, M.appendChild(B), M;
}
function no(l, u) {
  return u === "white" ? l : [7 - l[0], 7 - l[1]];
}
function au(l, u) {
  return (l && u.has(l) && u.get(l).size > 1) === !0;
}
function Pe(l) {
  return document.createElementNS("http://www.w3.org/2000/svg", l);
}
function He(l, u) {
  for (const s in u)
    Object.prototype.hasOwnProperty.call(u, s) && l.setAttribute(s, u[s]);
  return l;
}
function of(l, u) {
  return u ? {
    color: l.color,
    opacity: Math.round(l.opacity * 10) / 10,
    lineWidth: Math.round(u.lineWidth || l.lineWidth),
    key: [l.key, u.lineWidth].filter((s) => s).join("")
  } : l;
}
function mh() {
  return [3 / 64, 4 / 64];
}
function vh(l, u) {
  return (l.lineWidth || 10) * (u ? 0.85 : 1) / 64;
}
function uf(l, u) {
  return (l.opacity || 1) * (u ? 0.9 : 1);
}
function gh(l) {
  return (l ? 20 : 10) / 64;
}
function to(l, u) {
  const s = Math.min(1, u.width / u.height), c = Math.min(1, u.height / u.width);
  return [(l[0] - 3.5) * s, (3.5 - l[1]) * c];
}
function yh(l, u) {
  const s = {
    from: [Math.floor(Math.min(l[0], u[0])), Math.floor(Math.min(l[1], u[1]))],
    to: [Math.ceil(Math.max(l[0], u[0])), Math.ceil(Math.max(l[1], u[1]))]
  };
  return He(Pe("rect"), {
    x: s.from[0],
    y: s.from[1],
    width: s.to[0] - s.from[0],
    height: s.to[1] - s.from[1],
    fill: "none",
    stroke: "none"
  });
}
function cu(l, u, s = !0) {
  const c = Math.atan2(u[1] - l[1], u[0] - l[0]) + Math.PI;
  return s ? (Math.round(c * 8 / Math.PI) + 16) % 16 : c;
}
function wh(l, u) {
  return Math.sqrt([l[0] - u[0], l[1] - u[1]].reduce((s, c) => s + c * c, 0));
}
function sf(l, u, s) {
  let c = wh(l, u);
  const f = cu(l, u, !1);
  if (s && (c -= 33 / 64, s.size > 1)) {
    c -= 10 / 64;
    const m = cu(l, u);
    (s.has((m + 1) % 16) || s.has((m + 15) % 16)) && m & 1 && (c -= 0.4);
  }
  return [l[0] - Math.cos(f) * c, l[1] - Math.sin(f) * c].map((m) => m + 0.5);
}
function kh(l, u) {
  l.innerHTML = "", l.classList.add("cg-wrap");
  for (const z of vp)
    l.classList.toggle("orientation-" + z, u.orientation === z);
  l.classList.toggle("manipulable", !u.viewOnly);
  const s = jn("cg-container");
  l.appendChild(s);
  const c = jn("cg-board");
  s.appendChild(c);
  let f, m, k;
  if (u.drawable.visible && (f = He(Pe("svg"), {
    class: "cg-shapes",
    viewBox: "-4 -4 8 8",
    preserveAspectRatio: "xMidYMid slice"
  }), f.appendChild(lh()), f.appendChild(Pe("g")), m = He(Pe("svg"), {
    class: "cg-custom-svgs",
    viewBox: "-3.5 -3.5 8 8",
    preserveAspectRatio: "xMidYMid slice"
  }), m.appendChild(Pe("g")), k = jn("cg-auto-pieces"), s.appendChild(f), s.appendChild(m), s.appendChild(k)), u.coordinates) {
    const z = u.orientation === "black" ? " black" : "", S = u.ranksPosition === "left" ? " left" : "";
    if (u.coordinatesOnSquares) {
      const j = u.orientation === "white" ? (M) => M + 1 : (M) => 8 - M;
      Zl.forEach((M, B) => s.appendChild(ru(Jl.map(($) => M + $), "squares rank" + j(B) + z + S)));
    } else
      s.appendChild(ru(Jl, "ranks" + z + S)), s.appendChild(ru(Zl, "files" + z));
  }
  let E;
  return u.draggable.enabled && u.draggable.showGhost && (E = jn("piece", "ghost"), hu(E, !1), s.appendChild(E)), {
    board: c,
    container: s,
    wrap: l,
    ghost: E,
    svg: f,
    customSvg: m,
    autoPieces: k
  };
}
function ru(l, u) {
  const s = jn("coords", u);
  let c;
  for (const f of l)
    c = jn("coord"), c.textContent = f, s.appendChild(c);
  return s;
}
function Sh(l, u) {
  if (!l.dropmode.active)
    return;
  lt(l), ot(l);
  const s = l.dropmode.piece;
  if (s) {
    l.pieces.set("a0", s);
    const c = St(u), f = c && Ct(c, Ze(l), l.dom.bounds());
    f && Kc(l, "a0", f);
  }
  l.dom.redraw();
}
function Ch(l, u) {
  const s = l.dom.elements.board;
  if ("ResizeObserver" in window && new ResizeObserver(u).observe(l.dom.elements.wrap), (l.disableContextMenu || l.drawable.enabled) && s.addEventListener("contextmenu", (f) => f.preventDefault()), l.viewOnly)
    return;
  const c = _h(l);
  s.addEventListener("touchstart", c, {
    passive: !1
  }), s.addEventListener("mousedown", c, {
    passive: !1
  });
}
function Eh(l, u) {
  const s = [];
  if ("ResizeObserver" in window || s.push(Or(document.body, "chessground.resize", u)), !l.viewOnly) {
    const c = Tc(l, bp, Qp), f = Tc(l, eh, Kp);
    for (const k of ["touchmove", "mousemove"])
      s.push(Or(document, k, c));
    for (const k of ["touchend", "mouseup"])
      s.push(Or(document, k, f));
    const m = () => l.dom.bounds.clear();
    s.push(Or(document, "scroll", m, { capture: !0, passive: !0 })), s.push(Or(window, "resize", m, { passive: !0 }));
  }
  return () => s.forEach((c) => c());
}
function Or(l, u, s, c) {
  return l.addEventListener(u, s, c), () => l.removeEventListener(u, s, c);
}
const _h = (l) => (u) => {
  l.draggable.current ? bl(l) : l.drawable.current ? nf(l) : u.shiftKey || Fc(u) ? l.drawable.enabled && $p(l, u) : l.viewOnly || (l.dropmode.active ? Sh(l, u) : Gp(l, u));
}, Tc = (l, u, s) => (c) => {
  l.drawable.current ? l.drawable.enabled && s(l, c) : l.viewOnly || u(l, c);
};
function xh(l) {
  const u = Ze(l), s = jr(l.dom.bounds()), c = l.dom.elements.board, f = l.pieces, m = l.animation.current, k = m ? m.plan.anims : /* @__PURE__ */ new Map(), E = m ? m.plan.fadings : /* @__PURE__ */ new Map(), z = l.draggable.current, S = Nh(l), j = /* @__PURE__ */ new Set(), M = /* @__PURE__ */ new Set(), B = /* @__PURE__ */ new Map(), $ = /* @__PURE__ */ new Map();
  let Q, O, Y, ve, ue, Le, we, pe, Ce, Ee;
  for (O = c.firstChild; O; ) {
    if (Q = O.cgKey, af(O))
      if (Y = f.get(Q), ue = k.get(Q), Le = E.get(Q), ve = O.cgPiece, O.cgDragging && (!z || z.orig !== Q) && (O.classList.remove("dragging"), Nn(O, s(de(Q), u)), O.cgDragging = !1), !Le && O.cgFading && (O.cgFading = !1, O.classList.remove("fading")), Y) {
        if (ue && O.cgAnimating && ve === Ir(Y)) {
          const G = de(Q);
          G[0] += ue[2], G[1] += ue[3], O.classList.add("anim"), Nn(O, s(G, u));
        } else O.cgAnimating && (O.cgAnimating = !1, O.classList.remove("anim"), Nn(O, s(de(Q), u)), l.addPieceZIndex && (O.style.zIndex = lu(de(Q), u)));
        ve === Ir(Y) && (!Le || !O.cgFading) ? j.add(Q) : Le && ve === Ir(Le) ? (O.classList.add("fading"), O.cgFading = !0) : ou(B, ve, O);
      } else
        ou(B, ve, O);
    else if (cf(O)) {
      const G = O.className;
      S.get(Q) === G ? M.add(Q) : ou($, G, O);
    }
    O = O.nextSibling;
  }
  for (const [G, Be] of S)
    if (!M.has(G)) {
      Ce = $.get(Be), Ee = Ce && Ce.pop();
      const ke = s(de(G), u);
      if (Ee)
        Ee.cgKey = G, Nn(Ee, ke);
      else {
        const Ne = jn("square", Be);
        Ne.cgKey = G, Nn(Ne, ke), c.insertBefore(Ne, c.firstChild);
      }
    }
  for (const [G, Be] of f)
    if (ue = k.get(G), !j.has(G))
      if (we = B.get(Ir(Be)), pe = we && we.pop(), pe) {
        pe.cgKey = G, pe.cgFading && (pe.classList.remove("fading"), pe.cgFading = !1);
        const ke = de(G);
        l.addPieceZIndex && (pe.style.zIndex = lu(ke, u)), ue && (pe.cgAnimating = !0, pe.classList.add("anim"), ke[0] += ue[2], ke[1] += ue[3]), Nn(pe, s(ke, u));
      } else {
        const ke = Ir(Be), Ne = jn("piece", ke), Ae = de(G);
        Ne.cgPiece = ke, Ne.cgKey = G, ue && (Ne.cgAnimating = !0, Ae[0] += ue[2], Ae[1] += ue[3]), Nn(Ne, s(Ae, u)), l.addPieceZIndex && (Ne.style.zIndex = lu(Ae, u)), c.appendChild(Ne);
      }
  for (const G of B.values())
    Rc(l, G);
  for (const G of $.values())
    Rc(l, G);
}
function Ph(l) {
  const u = Ze(l), s = jr(l.dom.bounds());
  let c = l.dom.elements.board.firstChild;
  for (; c; )
    (af(c) && !c.cgAnimating || cf(c)) && Nn(c, s(de(c.cgKey), u)), c = c.nextSibling;
}
function Lc(l) {
  var u, s;
  const c = l.dom.elements.wrap.getBoundingClientRect(), f = l.dom.elements.container, m = c.height / c.width, k = Math.floor(c.width * window.devicePixelRatio / 8) * 8 / window.devicePixelRatio, E = k * m;
  f.style.width = k + "px", f.style.height = E + "px", l.dom.bounds.clear(), (u = l.addDimensionsCssVarsTo) === null || u === void 0 || u.style.setProperty("---cg-width", k + "px"), (s = l.addDimensionsCssVarsTo) === null || s === void 0 || s.style.setProperty("---cg-height", E + "px");
}
const af = (l) => l.tagName === "PIECE", cf = (l) => l.tagName === "SQUARE";
function Rc(l, u) {
  for (const s of u)
    l.dom.elements.board.removeChild(s);
}
function lu(l, u) {
  const c = l[1];
  return `${u ? 10 - c : 3 + c}`;
}
const Ir = (l) => `${l.color} ${l.role}`;
function Nh(l) {
  var u, s, c;
  const f = /* @__PURE__ */ new Map();
  if (l.lastMove && l.highlight.lastMove)
    for (const E of l.lastMove)
      Fn(f, E, "last-move");
  if (l.check && l.highlight.check && Fn(f, l.check, "check"), l.selected && (Fn(f, l.selected, "selected"), l.movable.showDests)) {
    const E = (u = l.movable.dests) === null || u === void 0 ? void 0 : u.get(l.selected);
    if (E)
      for (const S of E)
        Fn(f, S, "move-dest" + (l.pieces.has(S) ? " oc" : ""));
    const z = (c = (s = l.premovable.customDests) === null || s === void 0 ? void 0 : s.get(l.selected)) !== null && c !== void 0 ? c : l.premovable.dests;
    if (z)
      for (const S of z)
        Fn(f, S, "premove-dest" + (l.pieces.has(S) ? " oc" : ""));
  }
  const m = l.premovable.current;
  if (m)
    for (const E of m)
      Fn(f, E, "current-premove");
  else l.predroppable.current && Fn(f, l.predroppable.current.key, "current-premove");
  const k = l.exploding;
  if (k)
    for (const E of k.keys)
      Fn(f, E, "exploding" + k.stage);
  return l.highlight.custom && l.highlight.custom.forEach((E, z) => {
    Fn(f, z, E);
  }), f;
}
function Fn(l, u, s) {
  const c = l.get(u);
  c ? l.set(u, `${c} ${s}`) : l.set(u, s);
}
function ou(l, u, s) {
  const c = l.get(u);
  c ? c.push(s) : l.set(u, [s]);
}
function zh(l, u, s) {
  const c = /* @__PURE__ */ new Map(), f = [];
  for (const E of l)
    c.set(E.hash, !1);
  let m = u.firstElementChild, k;
  for (; m; )
    k = m.getAttribute("cgHash"), c.has(k) ? c.set(k, !0) : f.push(m), m = m.nextElementSibling;
  for (const E of f)
    u.removeChild(E);
  for (const E of l)
    c.get(E.hash) || u.appendChild(s(E));
}
function Mh(l, u) {
  const c = l.drawable.autoShapes.filter((f) => f.piece).map((f) => ({
    shape: f,
    hash: Rh(f),
    current: !1
  }));
  zh(c, u, (f) => Lh(l, f, l.dom.bounds()));
}
function Th(l) {
  var u;
  const s = Ze(l), c = jr(l.dom.bounds());
  let f = (u = l.dom.elements.autoPieces) === null || u === void 0 ? void 0 : u.firstChild;
  for (; f; )
    Ic(f, c(de(f.cgKey), s), f.cgScale), f = f.nextSibling;
}
function Lh(l, { shape: u, hash: s }, c) {
  var f, m, k;
  const E = u.orig, z = (f = u.piece) === null || f === void 0 ? void 0 : f.role, S = (m = u.piece) === null || m === void 0 ? void 0 : m.color, j = (k = u.piece) === null || k === void 0 ? void 0 : k.scale, M = jn("piece", `${z} ${S}`);
  return M.setAttribute("cgHash", s), M.cgKey = E, M.cgScale = j, Ic(M, jr(c)(de(E), Ze(l)), j), M;
}
const Rh = (l) => {
  var u, s, c;
  return [l.orig, (u = l.piece) === null || u === void 0 ? void 0 : u.role, (s = l.piece) === null || s === void 0 ? void 0 : s.color, (c = l.piece) === null || c === void 0 ? void 0 : c.scale].join(",");
};
function Dc(l, u) {
  const s = rh();
  Jc(s, u || {});
  function c() {
    const f = "dom" in s ? s.dom.unbind : void 0, m = kh(l, s), k = yp(() => m.board.getBoundingClientRect()), E = (j) => {
      xh(S), m.autoPieces && Mh(S, m.autoPieces), !j && m.svg && oh(S, m.svg, m.customSvg);
    }, z = () => {
      Lc(S), Ph(S), m.autoPieces && Th(S);
    }, S = s;
    return S.dom = {
      elements: m,
      bounds: k,
      redraw: Dh(E),
      redrawNow: E,
      unbind: f
    }, S.drawable.prevSvgHash = "", Lc(S), E(!1), Ch(S, z), f || (S.dom.unbind = Eh(S, z)), S.events.insert && S.events.insert(m), S;
  }
  return th(c(), c);
}
function Dh(l) {
  let u = !1;
  return () => {
    u || (u = !0, requestAnimationFrame(() => {
      l(), u = !1;
    }));
  };
}
const Oh = ({
  fen: l,
  setStateValue: u
}) => {
  const s = Gl.useRef(null);
  return Gl.useEffect(() => {
    if (!s.current) return;
    const c = Dc(s.current, {
      orientation: "white",
      coordinates: !0,
      movable: {
        free: !1,
        color: "both"
      },
      highlight: {
        lastMove: !0,
        check: !0
      },
      /**
       * Callback de movimento (origem → destino)
       * Aqui nasce o lance UCI.
       */
      events: {
        move: (f, m) => {
          const k = `${f}${m}`;
          u("uci_move", k);
        }
      }
    });
    return () => {
      c.destroy?.();
    };
  }, [u]), Gl.useEffect(() => {
    s.current && Dc(s.current).set({
      fen: l
    });
  }, [l]), /* @__PURE__ */ iu.jsx(
    "div",
    {
      ref: s,
      style: {
        width: "480px",
        height: "480px",
        margin: "0 auto"
      }
    }
  );
}, Xl = /* @__PURE__ */ new WeakMap(), Ih = (l) => {
  const { data: u, parentElement: s, setStateValue: c } = l, f = s.querySelector(".react-root");
  if (!f)
    throw new Error("Unexpected: React root element not found");
  let m = Xl.get(s);
  m || (m = mp.createRoot(f), Xl.set(s, m));
  const { fen: k } = u;
  return m.render(
    /* @__PURE__ */ iu.jsx(Gl.StrictMode, { children: /* @__PURE__ */ iu.jsx(Oh, { setStateValue: c, fen: k }) })
  ), () => {
    const E = Xl.get(s);
    E && (E.unmount(), Xl.delete(s));
  };
};
export {
  Ih as default
};
