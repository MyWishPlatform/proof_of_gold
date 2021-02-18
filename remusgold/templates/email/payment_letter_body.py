order_style = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Proof of Gold</title>
    <style type="text/css">
      body {
        margin: 0;
        padding: 0;
        min-width: 100% !important;
        font-family: sans-serif;
        background: #000;
        color: white;
      }

      img {
        height: auto;
      }

      .content {
        width: 100%;
        max-width: 660px;
      }

      .header {
        text-align: center;
        padding: 20px;
      }

      .info {
        padding: 40px 0px;
        text-align: center;
      }

      .text--center {
        text-align: center;
      }

      .text {
        font-size: 15px;
        line-height: 17px;
      }
      .text-footer {
        font-size: 10px;
        line-height: 11px;
        color: #737373;
        text-align: center;
      }
      .text-md {
        font-size: 16px;
        line-height: 18px;
      }
      .text-bold {
        font-weight: 700;
      }
      .code {
        color: #1737a0;
        padding-top: 5px;
      }

      .transparent {
        color: transparent;
        opacity: 0.5;
      }

      .footer {
        background: #202020;
        padding: 20px 0;
      }

      .container {
        padding: 30px;
        background: #202020;
      }

      .text-cont {
        padding-top: 25px;
      }
      .text-group {
        padding-top: 15px;
      }
      .text-sm {
        font-size: 12px;
        line-height: 14px;
      }

      .link {
        color: #fac929;
        font-size: 18px;
        line-height: 21px;
      }

      .link-md {
        color: #fac929;
        font-size: 12px;
        line-height: 14px;
      }
      .text-yellow {
        color: #fac929;
      }

      .accent {
        padding: 10px 0 0px 0;
        font-size: 25px;
        font-weight: 700;
        color: #fac929;
        text-transform: uppercase;
        text-align: center;
      }

      table {
        border-collapse: separate;
      }
    </style>
  </head>"""
order_body = """<body ducatus bgcolor="#000">
    <table
      width="100%"
      bgcolor="#000"
      border="0"
      cellpadding="0"
      cellspacing="0"
    >
      <tr>
        <td>
          <table
            bgcolor="#000"
            class="content"
            align="center"
            cellpadding="0"
            cellspacing="0"
            border="0"
          >
            <tr>
              <td style="border-radius: 0px" class="header">
                <img
                  class="fix"
                  src="https://proofofgold.herokuapp.com/logo-mail.svg"
                  width="108"
                  height="80"
                  border="0"
                  alt=""
                />
              </td>
            </tr>
            <tr>
              <td style="padding-bottom: 50px">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="accent">
                      Your order is confirmed (ORDER NUMBER)
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td class="container">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="text text-bold">Hello!</td>
                  </tr>
                  <tr>
                    <td class="text text-cont">
                      Thank you for ordering from POG!
                    </td>
                  </tr>
                  <tr>
                    <td class="text text-group">
                      Here’s a confirmation of the details of your order:
                    </td>
                  </tr>
                  <tr>
                    <td class="text text-group">
                      Name: <span class="text-yellow">{first_name} {last_name}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Email: <span class="text-yellow"> {email}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Phone: <span class="text-yellow">{phone}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Delivery Address: <span class="text-yellow">{delivery_address}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Shipping Option:
                      <span class="text-yellow">Priority Delivery</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="text text-group">
                      We aim to deliver your order within 3-5 weeks. Once we
                      have received your payment and checked with our Production
                      Team, we would be able to give you a fixed delivery date.
                      A member of our team may contact you by email should there
                      be any special shipping conditions in your country. Total
                      Paid Amount does not include duties and taxes (please
                      refer to the Terms and Conditions for more information).
                      Any import duties, taxes or fees due at the time of
                      delivery, as required in the specific country of
                      destination, are the sole responsibility of the receiving
                      customer. 
                    </td>
                  </tr>
"""
item_body = """<tr>
                    <td class="text text-group">
                      Item:
                      <span class="text-yellow">{item_name}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Weight: <span class="text-yellow">{weight}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Paid Amount: <span class="text-yellow">USD {amount}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Paid by: <span class="text-yellow">{paid_by}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Bonus Ducatus Coins: <span class="text-yellow">{bonus}%</span>
                    </td>
                  </tr>
"""

ending_body = """<tr>
                    <td class="text text-group text-yellow">
                      How to redeem Ducatus Coins:
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Open your Ducatus Wallet, click on Voucher > New Voucher.
                    </td>
                  </tr>
                  <tr>
                    <td class="text">
                      Input this Confirmation Code {code} and the address of
                      the wallet where you want to send your Ducatus Coins.
                    </td>
                  </tr>
                  <tr>
                    <td class="text">Finally, click Activate.</td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td class="info">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="text-sm">
                      Don’t have a Ducatus Wallet yet? Create one now!
                    </td>
                  </tr>
                  <tr>
                    <td class="text-sm text-group">Web Wallet</td>
                  </tr>
                  <tr>
                    <td class="text-md text-group text-bold">
                      <a class="link" href="https://wallet.ducatus.io"
                        >https://wallet.ducatus.io</a
                      >
                    </td>
                  </tr>
                  <tr>
                    <td class="text-sm text-cont">Mobile</td>
                  </tr>
                  <tr>
                    <td class="text-sm">
                      Download the
                      <a class="link-md" href="https://wallet.ducatus.io"
                        >Ducatus Wallet</a
                      >
                      app on
                      <a
                        class="link-md"
                        href="https://play.google.com/store/apps/details?id=io.ducatus.walnew&hl=ru&gl=US"
                        >Google Play</a
                      >
                      or
                      <a
                        class="link-md"
                        href="https://apps.apple.com/us/app/ducatus-wallet-2-0/id1489722627"
                        >App Store.</a
                      >
                    </td>
                  </tr>
                  <tr>
                    <td style="padding-top: 10px">
                      <a
                        class="transparent"
                        href="https://play.google.com/store/apps/details?id=io.ducatus.walnew&hl=ru&gl=US"
                      >
                        <img
                          src="https://proofofgold.herokuapp.com/google.svg"
                          alt=""
                        />
                      </a>
                      <a
                        class="transparent"
                        href="https://apps.apple.com/us/app/ducatus-wallet-2-0/id1489722627"
                      >
                        <img
                          src="https://proofofgold.herokuapp.com/apple.svg"
                          alt=""
                        />
                      </a>
                    </td>
                  </tr>
                  <tr>
                    <td class="text-sm text-cont">
                      Questions? Please email us at
                      <a href="mailto:INFO@D-POG.com" class="link-md"
                        >INFO@D-POG.com</a
                      >
                    </td>
                  </tr>
                  <tr>
                    <td class="text-md text-cont text-bold">The POG Team</td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td class="footer">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="text-footer">
                      @2020 Proof of Gold All rights reserved.
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""