def get_contact_html(feedback, usermail, username):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Contact Notification</title>
        <style type="text/css">
            /* Your email client may not use this CSS, inline styles are recommended for email templates */
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f4;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td style="padding: 20px 0 30px 0;">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #eaeaea; background-color: #ffffff;">
                        <tr>
                            <td align="center" bgcolor="#1A82E2" style="padding: 40px 0 30px 0; color: #ffffff; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;">
                                <img src="https://brown-planned-manatee-865.mypinata.cloud/ipfs/QmUKJWo7CLPs4fCUZ1aARHQ3SdparVHnRm4rATWKV28uM6" alt="Company Logo" width="300" height="90" style="display: block;" />
                            </td>
                        </tr>
                        <tr>
                            <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px; font-family: Arial, sans-serif;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td style="color: #153643; font-size: 24px;">
                                            <b>Contact Received</b>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 25px 0 0 0; color: #153643; font-size: 16px; line-height: 20px;">
                                            Hello Administrator,
                                            <br><br>
                                            You have a new Contact submission. The details are provided below.
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 20px 0 10px 0;">
                                            <hr style="border: 1px solid #eaeaea;">
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="color: #153643; font-size: 16px; line-height: 24px; padding: 5px 0;">
                                            <strong>Name:</strong>
                                            <br>
                                            {username}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="color: #153643; font-size: 16px; line-height: 24px; padding: 5px 0;">
                                            <strong>Email:</strong>
                                            <br>
                                            {usermail}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="color: #153643; font-size: 16px; line-height: 24px; padding: 20px 0;">
                                            <strong>Contact:</strong>
                                            <br>
                                            <div style="border-left: 3px solid #1A82E2; padding: 10px; margin-top: 10px; background-color: #f9f9f9;">
                                                {feedback_text}
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td bgcolor="#1A82E2" style="padding: 30px 30px 30px 30px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" align="center">
                                            &copy; 2024 Talkhealth.AI. All rights reserved.
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
    html_content = html_content.format(username=username, usermail=usermail, feedback_text=feedback)
    return html_content


def get_Reset_html(feedback, usermail):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Password Reset Notification</title>
        <style type="text/css">
            /* Your email client may not use this CSS, inline styles are recommended for email templates */
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f4;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td style="padding: 20px 0 30px 0;">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #eaeaea; background-color: #ffffff;">
                        <tr>
                            <td align="center" bgcolor="#1A82E2" style="padding: 40px 0 30px 0; color: #ffffff; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;">
                                <img src="https://brown-planned-manatee-865.mypinata.cloud/ipfs/QmUKJWo7CLPs4fCUZ1aARHQ3SdparVHnRm4rATWKV28uM6" alt="Company Logo" width="300" height="90" style="display: block;" />
                            </td>
                        </tr>
                        <tr>
                            <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px; font-family: Arial, sans-serif;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td style="color: #153643; font-size: 24px;">
                                            <b>Reset Password Email Received</b>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 25px 0 0 0; color: #153643; font-size: 16px; line-height: 20px;">
                                            Hello Administrator,
                                            <br><br>
                                            Follow this link to reset your Task Health AI password for your {usermail} account.
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td style="color: #153643; font-size: 16px; line-height: 24px; padding: 20px 0;">
                                            <strong>Reset Link:</strong>
                                            <br>
                                            <div style="border-left: 3px solid #1A82E2; padding: 10px; margin-top: 10px; background-color: #f9f9f9;">
                                                {feedback_text}
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td bgcolor="#1A82E2" style="padding: 30px 30px 30px 30px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" align="center">
                                            &copy; 2024 Talkhealth.AI. All rights reserved.
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
    html_content = html_content.format(usermail=usermail, feedback_text=feedback)
    return html_content


def get_feedback_html(feedback, rate, usermail, username):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Feedback Notification</title>
        <style type="text/css">
            /* Your email client may not use this CSS, inline styles are recommended for email templates */
        </style>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f4;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td style="padding: 20px 0 30px 0;">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #eaeaea; background-color: #ffffff;">
                        <tr>
                            <td align="center" bgcolor="#1A82E2" style="padding: 40px 0 30px 0; color: #ffffff; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;">
                                <img src="https://brown-planned-manatee-865.mypinata.cloud/ipfs/QmUKJWo7CLPs4fCUZ1aARHQ3SdparVHnRm4rATWKV28uM6" alt="Company Logo" width="300" height="90" style="display: block;" />
                            </td>
                        </tr>
                        <tr>
                            <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px; font-family: Arial, sans-serif;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td style="color: #153643; font-size: 24px;">
                                            <b>Feedback Received</b>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 25px 0 0 0; color: #153643; font-size: 16px; line-height: 20px;">
                                            Hello Administrator,
                                            <br><br>
                                            You have a new feedback submission. The details are provided below.
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 20px 0 10px 0;">
                                            <hr style="border: 1px solid #eaeaea;">
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="color: #153643; font-size: 16px; line-height: 24px; padding: 5px 0;">
                                            <strong>Name:</strong>
                                            <br>
                                            {username}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="color: #153643; font-size: 16px; line-height: 24px; padding: 5px 0;">
                                            <strong>Email:</strong>
                                            <br>
                                            {usermail}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="color: #153643; font-size: 16px; line-height: 24px; padding: 20px 0;">
                                            <strong>Feedback:</strong>
                                            <br>
                                            <div style="border-left: 3px solid #1A82E2; padding: 10px; margin-top: 10px; background-color: #f9f9f9;">
                                                {feedback_text}
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td bgcolor="#1A82E2" style="padding: 30px 30px 30px 30px;">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" align="center">
                                            &copy; 2024 Talkhealth.AI. All rights reserved.
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
    html_content = html_content.format(username=username, usermail=usermail, feedback_text=feedback)
    return html_content


def get_summarization_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document Summary</title>
    </head>
    <body>
        <header class="document-header">
            <div class="logo-container">
                <img src="{logo}" alt="My Image" class="document-logo">
            </div>
            <div class="header-info">
                <h1>Empowering Your Health</h1>
            </div>
        </header>

        <div class="content">
            <main class="document-body">
                <section class="body-info">
                    {text}
                </section>
            </main>
        </div>

        <footer class="document-footer">
            <div class="footer-info">
                <strong>TalkHealth.ai</strong>
                <p>info@talkhealth.ai</p>
            </div>
            <div class="footer-disclaimer">
                <p><strong>Disclaimer:</strong> This tool and its content are not medical advice. This is AI 
technology that does not replace a real medical professional. Always 
consult a medical doctor with your health questions.</p>
            </div>
        </footer>
    </body>
    </html>
    """
    
    return html_content
