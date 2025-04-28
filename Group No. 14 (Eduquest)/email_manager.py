from __future__ import print_function
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pprint import pprint
import config

# Try to import Brevo SDK, but provide fallback option
try:
    import sib_api_v3_sdk
    from sib_api_v3_sdk.rest import ApiException
    BREVO_SDK_AVAILABLE = True
except ImportError:
    print("Brevo SDK not available. Using fallback email mechanism.")
    BREVO_SDK_AVAILABLE = False

class EmailManager:
    def __init__(self, api_key=None):
        """Initialize the EmailManager with Brevo API credentials"""
        self.api_key = api_key or config.BREVO_API_KEY
        self.sender = config.EMAIL_SENDER
        
        # Configure the appropriate email mechanism
        if BREVO_SDK_AVAILABLE:
            self.configure_brevo_api()
        else:
            # Configure SMTP settings for fallback
            self.smtp_server = config.SMTP_CONFIG.get('server', 'smtp.gmail.com')
            self.smtp_port = config.SMTP_CONFIG.get('port', 587)
            self.smtp_username = config.SMTP_CONFIG.get('username', '')
            self.smtp_password = config.SMTP_CONFIG.get('password', '')
        
    def configure_brevo_api(self):
        """Configure the Brevo API client"""
        sib_api_v3_sdk.configuration.api_key['api-key'] = self.api_key
        self.email_api = sib_api_v3_sdk.EmailCampaignsApi()
        self.smtp_api = sib_api_v3_sdk.TransactionalEmailsApi()
        
    def send_welcome_email(self, user_email, username):
        """Send a welcome email to a new user"""
        # Create email content
        subject = "Welcome to EduQuest!"
        html_content = f"""
        <html>
        <body>
            <h1>Welcome to EduQuest, {username}!</h1>
            <p>Thank you for creating an account with us. We're excited to have you join our community of learners!</p>
            <p>With EduQuest, you can:</p>
            <ul>
                <li>Access mock tests for CET and JEE examinations</li>
                <li>Track your progress and analyze your performance</li>
                <li>Get personalized study recommendations</li>
            </ul>
            <p>If you have any questions, please don't hesitate to reach out to our support team.</p>
            <p>Happy learning!</p>
            <p>The EduQuest Team</p>
        </body>
        </html>
        """
        
        # Choose the method based on SDK availability
        if BREVO_SDK_AVAILABLE:
            return self._send_welcome_email_brevo(user_email, username, subject, html_content)
        else:
            return self._send_welcome_email_smtp(user_email, username, subject, html_content)
    
    def _send_welcome_email_brevo(self, user_email, username, subject, html_content):
        """Send welcome email using Brevo API"""
        try:
            # Create a send email object
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": user_email, "name": username}],
                sender=self.sender,
                subject=subject,
                html_content=html_content
            )
            
            # Make the API call
            api_response = self.smtp_api.send_transac_email(send_smtp_email)
            print(f"Welcome email sent to {user_email} using Brevo API")
            return True, api_response
            
        except ApiException as e:
            print(f"Exception when sending welcome email: {e}")
            return False, str(e)
    
    def _send_welcome_email_smtp(self, user_email, username, subject, html_content):
        """Send welcome email using standard SMTP"""
        try:
            # Create MIME message
            msg = MIMEMultipart()
            msg['From'] = f"{self.sender['name']} <{self.sender['email']}>"
            msg['To'] = f"{username} <{user_email}>"
            msg['Subject'] = subject
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Setup SMTP server connection
            try:
                # If SMTP configuration is available
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()  # Secure the connection
                
                # Login if credentials are provided
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                
                # Send the email
                server.send_message(msg)
                server.quit()
                print(f"Welcome email sent to {user_email} using SMTP")
                return True, "Email sent successfully via SMTP"
                
            except Exception as smtp_err:
                print(f"SMTP error: {smtp_err}")
                print("Attempting to save email locally instead...")
                
                # Fallback - save email to a file if SMTP fails
                try:
                    file_name = f"welcome_email_{username}_{int(time.time())}.html"
                    with open(file_name, 'w') as f:
                        f.write(f"To: {user_email}\nSubject: {subject}\n\n")
                        f.write(html_content)
                    print(f"Email saved to file: {file_name}")
                    return True, f"Email saved to file: {file_name}"
                except Exception as file_err:
                    print(f"File write error: {file_err}")
                    return False, str(file_err)
                
        except Exception as e:
            print(f"Exception when sending welcome email: {e}")
            return False, str(e)
    
    def create_email_campaign(self, name, subject, content, list_ids, scheduled_at=None):
        """Create an email campaign for multiple users"""
        if not BREVO_SDK_AVAILABLE:
            print("Email campaigns require the Brevo SDK. Please install with 'pip install sib-api-v3-sdk'")
            return False, "Brevo SDK not available"
            
        try:
            # Set default scheduled time if not provided (now + 1 hour)
            if not scheduled_at:
                scheduled_at = time.strftime("%Y-%m-%d %H:%M:%S", 
                                          time.localtime(time.time() + 3600))
            
            # Create email campaign object
            email_campaign = sib_api_v3_sdk.CreateEmailCampaign(
                name=name,
                subject=subject,
                sender=self.sender,
                type="classic",
                html_content=content,
                recipients={"listIds": list_ids},
                scheduled_at=scheduled_at
            )
            
            # Make the API call
            api_response = self.email_api.create_email_campaign(email_campaign)
            print(f"Campaign created: {name}")
            return True, api_response
            
        except ApiException as e:
            print(f"Exception when creating email campaign: {e}")
            return False, str(e) 