order_body = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Proof of Gold</title>
  </head>
  <body
    ducatus=""
    bgcolor="#000"
    style="
      margin: 0;
      padding: 0;
      min-width: 100%;
      font-family: sans-serif;
      background: #000;
    "
  >
    <table
      width="100%"
      bgcolor="#000"
      border="0"
      cellpadding="0"
      cellspacing="0"
      style="border-collapse: separate"
    >
      <tr>
        <td>
          <table
            bgcolor="#000"
            style="border-collapse: separate; width: 100%; max-width: 660px"
            align="center"
            cellpadding="0"
            cellspacing="0"
            border="0"
            width="100%"
          >
            <tr>
              <td style="border-radius: 0px; text-align: center; padding: 20px">
                <img
                  src="https://devgold.rocknblock.io/media/logo.png"
                  width="108"
                  height="80"
                  border="0"
                  alt=""
                  style="height: auto"
                />
              </td>
            </tr>
            <tr>
              <td style="padding-bottom: 50px">
                <table
                  width="100%"
                  border="0"
                  cellspacing="0"
                  cellpadding="0"
                  style="border-collapse: separate"
                >
                  <tr>
                    <td
                      style="
                        padding: 10px 0 0px 0;
                        font-size: 25px;
                        font-weight: 700;
                        color: #fac929;
                        text-transform: uppercase;
                        text-align: center;
                      "
                    >
                      Your order {order_number} is confirmed
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding: 30px; background: #202020">
                <table
                  width="100%"
                  border="0"
                  cellspacing="0"
                  cellpadding="0"
                  style="border-collapse: separate"
                >
                  <tr>
                    <td
                      style="
                        font-weight: 700;
                        font-size: 15px;
                        line-height: 17px;
                        color: white;
                      "
                      class="text text-bold"
                    >
                      Hello!
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text text-cont"
                      style="
                        font-size: 15px;
                        line-height: 17px;
                        color: white;
                        padding-top: 25px;
                      "
                    >
                      Thank you for ordering from POG!
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text text-group"
                      style="
                        font-size: 15px;
                        line-height: 17px;
                        color: white;
                        padding-top: 15px;
                      "
                    >
                      Here’s a confirmation of the details of your order:
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text text-group"
                      style="
                        font-size: 15px;
                        line-height: 17px;
                        color: white;
                        padding-top: 15px;
                      "
                    >
                      Name:
                      <span class="text-yellow" style="color: #fac929"
                        >{first_name} {last_name}</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Email:
                      <span class="text-yellow" style="color: #fac929">
                        {email}</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Phone:
                      <span class="text-yellow" style="color: #fac929"
                        >{phone}</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Delivery Address:
                      <span class="text-yellow" style="color: #fac929"
                        >{delivery_address}</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Shipping Option:
                      <span class="text-yellow" style="color: #fac929"
                        >Priority Delivery</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text text-group"
                      style="
                        font-size: 15px;
                        line-height: 17px;
                        color: white;
                        padding-top: 15px;
                      "
                    >
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
                    <td
                      class="text text-group"
                      style="
                        font-size: 15px;
                        line-height: 17px;
                        color: white;
                        padding-top: 15px;
                      "
                    >
                      Item:
                      <span class="text-yellow" style="color: #fac929"
                        >{item_name}</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Weight:
                      <span class="text-yellow" style="color: #fac929"
                        >{weight}</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Paid Amount:
                      <span class="text-yellow" style="color: #fac929"
                        >USD {amount}</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Paid by:
                      <span class="text-yellow" style="color: #fac929"
                        >{paid_by}</span
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Bonus Ducatus Coins:
                      <span class="text-yellow" style="color: #fac929"
                        >{bonus}%</span
                      >
                    </td>
                  </tr>
"""

ending_body = """<tr>
                    <td
                      class="text text-group text-yellow"
                      style="
                        font-size: 15px;
                        line-height: 17px;
                        color: #fac929;
                        padding-top: 15px;
                      "
                    >
                      How to redeem Ducatus Coins:
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Open your Ducatus Wallet, click on Voucher > New Voucher.
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Input this Confirmation Code 
                      <span style="color: #fac929">{code}</span> and the 
                      address of the wallet where you want to send your Ducatus Coins.
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text"
                      style="font-size: 15px; line-height: 17px; color: white"
                    >
                      Finally, click Activate.
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td
                class="info"
                style="padding: 40px 0px; text-align: center"
                align="center"
              >
                <table
                  width="100%"
                  border="0"
                  cellspacing="0"
                  cellpadding="0"
                  style="border-collapse: separate"
                >
                  <tr>
                    <td
                      class="text-sm"
                      style="font-size: 12px; line-height: 14px"
                    >
                      Don’t have a Ducatus Wallet yet? Create one now!
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text-sm text-group"
                      style="
                        padding-top: 15px;
                        font-size: 12px;
                        line-height: 14px;
                      "
                    >
                      Web Wallet
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text-md text-group text-bold"
                      style="
                        font-size: 16px;
                        line-height: 18px;
                        font-weight: 700;
                        padding-top: 15px;
                      "
                    >
                      <a
                        class="link"
                        href="https://wallet.ducatus.io"
                        style="
                          color: #fac929;
                          font-size: 18px;
                          line-height: 21px;
                        "
                        >https://wallet.ducatus.io</a
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text-sm text-cont"
                      style="
                        padding-top: 25px;
                        font-size: 12px;
                        line-height: 14px;
                      "
                    >
                      Mobile
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text-sm"
                      style="font-size: 12px; line-height: 14px; color: #fac929"
                    >
                      Download the
                      <a
                        class="link-md"
                        href="https://wallet.ducatus.io"
                        style="
                          color: #fac929;
                          font-size: 12px;
                          line-height: 14px;
                        "
                        >Ducatus Wallet</a
                      >
                      app on
                      <a
                        class="link-md"
                        href="https://play.google.com/store/apps/details?id=io.ducatus.walnew&hl=ru&gl=US"
                        style="
                          color: #fac929;
                          font-size: 12px;
                          line-height: 14px;
                        "
                        >Google Play</a
                      >
                      or
                      <a
                        class="link-md"
                        href="https://apps.apple.com/us/app/ducatus-wallet-2-0/id1489722627"
                        style="
                          color: #fac929;
                          font-size: 12px;
                          line-height: 14px;
                        "
                        >App Store.</a
                      >
                    </td>
                  </tr>
                  <tr>
                    <td style="padding-top: 10px">
                      <a
                        class="transparent"
                        href="https://play.google.com/store/apps/details?id=io.ducatus.walnew&hl=ru&gl=US"
                        style="color: transparent; opacity: 0.5"
                      >
                        <img
                          src="https://proofofgold.herokuapp.com/google.svg"
                          alt=""
                          style="height: auto"
                        />
                      </a>
                      <a
                        class="transparent"
                        href="https://apps.apple.com/us/app/ducatus-wallet-2-0/id1489722627"
                        style="color: transparent; opacity: 0.5"
                      >
                        <img
                          src="https://proofofgold.herokuapp.com/apple.svg"
                          alt=""
                          style="height: auto"
                        />
                      </a>
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text-sm text-cont"
                      style="
                        padding-top: 25px;
                        font-size: 12px;
                        line-height: 14px;
                        color: #fac929;
                      "
                    >
                      Questions? Please email us at
                      <a
                        href="mailto:INFO@D-POG.com"
                        class="link-md"
                        style="
                          color: #fac929;
                          font-size: 12px;
                          line-height: 14px;
                        "
                        >INFO@D-POG.com</a
                      >
                    </td>
                  </tr>
                  <tr>
                    <td
                      class="text-md text-cont text-bold"
                      style="
                        font-size: 16px;
                        line-height: 18px;
                        font-weight: 700;
                        padding-top: 25px;
                      "
                    >
                      The POG Team
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td class="footer" style="background: #202020; padding: 20px 0">
                <table
                  width="100%"
                  border="0"
                  cellspacing="0"
                  cellpadding="0"
                  style="border-collapse: separate"
                >
                  <tr>
                    <td
                      class="text-footer"
                      style="
                        font-size: 10px;
                        line-height: 11px;
                        color: #737373;
                        text-align: center;
                      "
                      align="center"
                    >
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