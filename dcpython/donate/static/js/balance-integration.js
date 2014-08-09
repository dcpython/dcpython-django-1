/* global jQuery, console, balanced, window */

jQuery(function($) {
    "use strict";

    var DONATION_AMTS = [
      ["platinum", 1000],
      ["gold", 500],
      ["silver", 250],
      ["bronze", 100],
      ["individual", 50],
      ["other", 0]
    ];

    var DONATION_AMTS_DICT = {
      platinum: 1000,
      gold: 500,
      silver: 250,
      bronze: 100,
      individual: 50,
      other: 25
    };

    // DONATION TEXTBOX VALUE CHANGE
    var handle_donation_change = function() {
      var i;
      var donation = parseFloat($("#donationAmt").val());
      for (i=0; i < DONATION_AMTS.length; i++) {
        $("." + DONATION_AMTS[i][0]).removeClass("active");
      }
      for (i=0; i < DONATION_AMTS.length; i++) {
        if (donation >= DONATION_AMTS[i][1]) {
          $("." + DONATION_AMTS[i][0]).addClass("active");
          break;
        }
      }
      $("#id_donation").val(donation);
    };

    $("#donationAmt").change(handle_donation_change).keyup(handle_donation_change);
    handle_donation_change();
    
    // LEVEL CLICKS
    var handle_donor_lvl_click = function(e) {
      var donation = DONATION_AMTS_DICT[$(e.currentTarget).attr("class").split(" ")[1]];

      $("#donationAmt").val(donation);
      handle_donation_change();
    };

    $(".donor_lvl").click(handle_donor_lvl_click);

    // DONATION SOURCE CHANGE
    var handle_donation_source_change = function(e) {
      var donation_source = $(e.target).val();

      $(".payment-form").addClass("hidden");
      $("#form-" + donation_source).removeClass("hidden");
      $("#id_donation_type").val(donation_source);
    };


    $("#donate_source").change(handle_donation_source_change);
    // need to do this so value is "B" at start
    $("#id_donation_type").val("B");

    // handle SUBMIT btn
    window.handle_submit_btn = function() {
      // first, disable submit button so no bouble submit
      $("#submit_btn").attr("disabled", "disabled");
      var donation_amount = $("#donationAmt").val();

      // validate amount first - 1 to 999999.99 dollars 
      // TODO this is not ideal b/c full form is not validated
      if (!/^[1-9][0-9]{0,5}(\.[0-9]{1,2})?$/.test(donation_amount)) {
        $("#donationAmt").parents(".form-group").addClass("has-error");
        $("#submit_btn").attr("disabled", null);
        return false;
      }

      var donation_type = $("#id_donation_type").val();

      // remove any errors, so can add just existing errors
      $(".form-group").removeClass("has-error");

      var form;

      // get bank token if trying to use bank
      if (donation_type == "B") {
        form = $("#form-B");
          
        var bankAccountData = {
          name: $("#name").val(),
          routing_number: $("#routing_number").val(),
          account_number: $("#account_number").val(),
          type: $("#bankAcctType").val()
        };
        balanced.bankAccount.create(bankAccountData, function(resp) {
          if (resp.error) {
            for (var k in resp.error) {
              $("#" + k).parents(".form-group").addClass("has-error");
            }
          } else if (resp.data) {
            $("#id_bank_token").val(resp.data.uri);
          }

          makeAjax();
        });
      // get cc token if trying to use cc
      } else if (donation_type == "C") {
        form = $("#form-C");

        var expiration = $("#expiration").val().split("/");

        var ccData = {
          card_number: $("#card_number").val(),
          expiration_month: expiration[0],
          expiration_year: expiration[1],
          security_code: $("#security_code").val()
        };

        balanced.card.create(ccData, function(resp) {
          if (resp.error) {
            for (var k in resp.error) {
              k = (k.indexOf("expiration") >= 0) ? "expiration" : k;
              $("#" + k).parents(".form-group").addClass("has-error");
            }
          } else if (resp.data) {
            $("#id_cc_token").val(resp.data.uri);
          }
          makeAjax();
        });

      }

      function makeAjax() {
        // Make AJAX request
        var data = {};
        $("#master_donate_form").find("input").each(function(w,x) {
          $x = $(x);
          data[$x.attr('name')] = $x.val();
        })
        // data = JSON.stringify(data);

        $.post("/make_donation", data, function(resp) {
          resp = JSON.parse(resp);
          if (resp.html) {
            $("#master_donate_div").html(resp.html);
          }
          else if (resp.error) {
            console.log("ERROR", resp.error);
          }
        });

        $("#submit_btn").attr("disabled", null);
      }
    return false;
    };

    $("#master_donate_form").submit(handle_submit_btn);

  });

