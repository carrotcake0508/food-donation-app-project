#lang racket

(require web-server/servlet
         web-server/servlet-env
         gregor
         racket/date)

(define root (current-directory))

(define avail-food-types '())
(define avail-food-quant '())
(define donor-contact+address-info '())
(define rqstd-food-types '())
(define rqstd-food-quant '())
(define rcpnt-cntct+lctn-info '())

(define (start request)
  (define (response-generator embed/url)
    (response/xexpr
     `(html
       (head (title "Pass the Plate")
             (link ((rel "stylesheet")
                  (href ,"/style.css")
                  (type "text/css"))))
       (body (h1 "Welcome to Pass the Plate!")
             (br)
             "We are a non-profit organization, providing the excess food of people with lots of resources to people in need of food. We link donor-provided food to drop-off locations throughout King County by volunteer food-transportation. Sign up to donate, recieve or volunteer!"
             (br)
             (a ((href ,(embed/url donate-food)))
                "Donate food here")
             (br)
             (a ((href ,(embed/url request-food)))
                "Request food here")
             (br)
             (a ((href ,(embed/url vol-pg)))
                "Volunteer deliverer page")
             (br)
             (h2 "Available food:")
             (table ((border "2"))
                    (tr (th "Food type") (th "Quantity"))
              ,@(for/list ((foodtype avail-food-types)
                           (foodquant avail-food-quant))
                  `(tr (td ,foodtype) (td ,foodquant))))
             (h2 "Requested food:")
             (table ((border "2"))
                    (tr (th "Food type") (th "Quantity"))
                    ,@(for/list ((foodtype rqstd-food-types)
                                 (foodquant rqstd-food-quant))
                        `(tr (td ,foodtype) (td ,foodquant))))))))
  (send/suspend/dispatch response-generator))
(define (donate-food request)
  (define (response-generator-2 embed/url)
    (response/xexpr
     `(html
       (head (title "Donor@Pass the Plate")
             (link ((rel "stylesheet")
                  (href ,"/style.css")
                  (type "text/css"))))
       (body (a ((href ,(embed/url start)))
                "Back to home page")
             (form ((action ,(embed/url register-food)))
                   "Food type:"
                   (input ((name "food-type")))
                   (br)
                   "Quantity:"
                   (input ((name "food-quantity")))
                   (br)
                   "Units:"
                   (input ((name "units")))
                   (br)
                   "Food expiration date (yyyy-dd-mm):"
                   (input ((name "expir-date")))
                   (br)
                   "Location (Street Address):"
                   (input ((name "location-info")))
                   (br)
                   "Phone #:"
                   (input ((name "phone-number")))
                   (input ((type "submit") (value "Register Food"))))))))
  (send/suspend/dispatch response-generator-2))
(define (request-food request)
  (define (response-generator-3 embed/url)
    (response/xexpr
     `(html
       (head (title "Recipient@Pass the Plate")
             (link ((rel "stylesheet")
                  (href ,"/style.css")
                  (type "text/css"))))
       (body (a ((href ,(embed/url start)))
                "Back to home page")
             (form ((action ,(embed/url get-food)))
                   "Food type:"
                   (input ((name "food-type")))
                   (br)
                   "Quantity:"
                   (input ((name "food-quantity")))
                   (br)
                   "Units:"
                   (input ((name "units")))
                   (br)
                   "Nearest drop-off location (see map on home page):"
                   (br)
                   (input ((name "nrst-drpoff-lctn")))
                   (br)
                   "Phone #:"
                   (br)
                   (input ((name "phone-number")))
                   (input ((type "submit") (value "Request Food"))))))))
  (send/suspend/dispatch response-generator-3))
(define (vol-pg request)
  (define (response-gen-5 embed/url)
    (response/xexpr
     `(html
       (head (title "Volunteer@Pass the Plate")
             (link ((rel "stylesheet")
                  (href ,"/style.css")
                  (type "text/css"))))
       (body (a ((href ,(embed/url start)))
                "Back to home page")
             (table ((border "2"))
                    (tr (th "Donor Info"))
                    ,@(for/list ((donor-info donor-contact+address-info))
                        `(tr (td ,donor-info)))
                    (tr (th "Recipient Info"))
                    ,@(for/list ((rcpnt-info rcpnt-cntct+lctn-info))
                        `(tr (td ,rcpnt-info))))))))
  (send/suspend/dispatch response-gen-5))
(define (register-food request)
  (define (response-gen-4 embed/url)
    (set! avail-food-types (cons (extract-binding/single 'food-type (request-bindings request)) avail-food-types))
    (set! avail-food-quant (cons (string-append (extract-binding/single 'food-quantity (request-bindings request)) " " (extract-binding/single 'units (request-bindings request))) avail-food-quant))
    (set! donor-contact+address-info (cons (string-append "On " (date->iso8601 (today)) " donor at " (extract-binding/single 'location-info (request-bindings request)) " donated " (extract-binding/single 'food-quantity (request-bindings request)) " " (extract-binding/single 'units (request-bindings request)) " of " (extract-binding/single 'food-type (request-bindings request)) " that expires on " (extract-binding/single 'expir-date (request-bindings request)) " under phone # " (extract-binding/single 'phone-number (request-bindings request))) donor-contact+address-info))
    (start request))
  (send/suspend/dispatch response-gen-4))
(define (get-food request)
  (define (response-gen-6 embed/url)
    (set! rqstd-food-types (cons (extract-binding/single 'food-type (request-bindings request)) rqstd-food-types))
    (set! rqstd-food-quant (cons (string-append (extract-binding/single 'food-quantity (request-bindings request)) " " (extract-binding/single 'units (request-bindings request))) rqstd-food-quant))
    (set! rcpnt-cntct+lctn-info (cons (string-append "On " (date->iso8601 (today)) " recipient near " (extract-binding/single 'nrst-drpoff-lctn (request-bindings request)) " requested " (extract-binding/single 'food-quantity (request-bindings request)) " " (extract-binding/single 'units (request-bindings request)) " of " (extract-binding/single 'food-type (request-bindings request)) " under phone # " (extract-binding/single 'phone-number (request-bindings request))) rcpnt-cntct+lctn-info))
    (start request))
  (send/suspend/dispatch response-gen-6))

(serve/servlet start
               #:extra-files-paths (list (build-path root)))