import os
import io
import mysql.connector
import platform
import tkinter as tk
from tkinter import messagebox, filedialog 
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class PDFExport:
    def export_to_pdf(self):
        # Show authentication dialog first
        auth_dialog = tk.Toplevel(self.root)
        auth_dialog.title("Authentication Required")
        auth_dialog.geometry("300x150")
        auth_dialog.configure(bg="#C9C7BA")
        auth_dialog.resizable(False, False)

        # Center the dialog
        auth_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50,
                                         self.root.winfo_rooty() + 50))

        # Authentication code entry
        auth_label = tk.Label(auth_dialog, text="Enter your authentication code:",
                              font=("Arial", 12), bg="#C9C7BA", fg="#29292B")
        auth_label.pack(pady=10)

        auth_entry = tk.Entry(auth_dialog, font=("Arial", 12), width=10, show="*")
        auth_entry.pack(pady=10)

        # Verify button
        verify_button = tk.Button(auth_dialog, text="Verify", font=("Arial", 12),bg="#29292B", fg="white",
                                  command=lambda: self.verify_export_auth(auth_entry.get(), auth_dialog))
        verify_button.pack(pady=10)


    def verify_export_auth(self, entered_code, dialog):
        try:
            # Get the stored auth code from database
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT auth_code FROM users WHERE id = %s", (self.current_user["id"],))
            stored_auth_code = cursor.fetchone()[0]
            conn.close()

            if entered_code == stored_auth_code:
                dialog.destroy()
                self.proceed_with_export()
            else:
                messagebox.showerror("Error", "Authentication failed")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


    def proceed_with_export(self):
        # Ask user where to save the PDF file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save Financial Report As"
        )

        if not file_path:
            return  # User cancelled

        # Get currency symbol
        currency_symbol = self.get_currency_symbol()

        # Create PDF exporter
        exporter = PDFExport(
            self.db_config,
            self.current_user["id"],
            self.current_user["username"],
            currency_symbol
        )

        # Show progress dialog
        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title("Exporting to PDF")
        progress_dialog.geometry("300x100")
        progress_dialog.configure(bg="#C9C7BA")
        progress_dialog.resizable(False, False)

        # Center the dialog
        progress_dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50,
                                             self.root.winfo_rooty() + 50))

        # Progress message
        progress_label = tk.Label(progress_dialog, text="Generating PDF report...",
                                  font=("Arial", 12), bg="#C9C7BA", fg="#29292B")
        progress_label.pack(pady=20)

        # Update the UI
        self.root.update()

        # Generate the PDF
        success = exporter.generate_pdf(file_path)

        # Close progress dialog
        progress_dialog.destroy()

        if success:
            messagebox.showinfo("Success", f"Financial report exported successfully to:\n{file_path}")

            # Ask if user wants to open the PDF
            if messagebox.askyesno("Open PDF", "Would you like to open the PDF now?"):
                try:
                    if platform.system() == 'Darwin':  # macOS
                        os.system(f'open "{file_path}"')
                    elif platform.system() == 'Windows':  # Windows
                        os.system(f'start "" "{file_path}"')
                    else:  # Linux
                        os.system(f'xdg-open "{file_path}"')
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open the PDF: {e}")
        else:
            messagebox.showerror("Error", "Failed to generate PDF report")
    
    def __init__(self, db_config, user_id, username, currency_symbol):
        self.db_config = db_config
        self.user_id = user_id
        self.username = username
        self.currency_symbol = currency_symbol
        self.styles = getSampleStyleSheet()
        
        # Create custom styles
        self.title_style = ParagraphStyle(
            'Title',
            parent=self.styles['Title'],
            fontSize=18,
            textColor=colors.darkblue,
            spaceAfter=12
        )
        
        self.heading_style = ParagraphStyle(
            'Heading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceAfter=6,
            spaceBefore=12
        )
        
        self.normal_style = ParagraphStyle(
            'Normal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
    
    def generate_pdf(self, output_path):
        import mysql.connector
        
        try:
            # Connect to database
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get user info
            cursor.execute("""
                SELECT username, email, currency 
                FROM users 
                WHERE id = %s
            """, (self.user_id,))
            user_info = cursor.fetchone()
            
            # Get summary data
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END), 0) as total_income,
                    COALESCE(SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END), 0) as total_expense
                FROM transactions 
                WHERE user_id = %s
            """, (self.user_id,))
            summary_data = cursor.fetchone()
            
            # Get transactions
            cursor.execute("""
                SELECT t.id, t.date, t.type, c.name, t.amount, t.description
                FROM transactions t 
                JOIN categories c ON t.category_id = c.id 
                WHERE t.user_id = %s 
                ORDER BY t.date DESC
            """, (self.user_id,))
            transactions = cursor.fetchall()
            
            # Get category data for pie chart
            cursor.execute("""
                SELECT c.name, SUM(t.amount), c.color
                FROM transactions t 
                JOIN categories c ON t.category_id = c.id 
                WHERE t.user_id = %s AND t.type = 'Expense'
                GROUP BY c.name, c.color
                ORDER BY SUM(t.amount) DESC
            """, (self.user_id,))
            category_data = cursor.fetchall()
            
            # Get monthly data for trend chart
            cursor.execute("""
                SELECT DATE_FORMAT(date, '%Y-%m') as month, 
                       SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) as income,
                       SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) as expense
                FROM transactions 
                WHERE user_id = %s
                GROUP BY month
                ORDER BY month
                LIMIT 12
            """, (self.user_id,))
            monthly_data = cursor.fetchall()
            
            conn.close()
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build content
            content = []
            
            # Title
            title = Paragraph(f"Financial Report - {user_info[0]}", self.title_style)
            content.append(title)
            
            # Date
            date_text = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.normal_style)
            content.append(date_text)
            content.append(Spacer(1, 0.2*inch))
            
            # User Information
            content.append(Paragraph("User Information", self.heading_style))
            user_data = [
                ["Username:", user_info[0]],
                ["Email:", user_info[1]],
                ["Currency:", user_info[2]]
            ]
            user_table = Table(user_data, colWidths=[1.5*inch, 4*inch])
            user_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (1, 0), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(user_table)
            content.append(Spacer(1, 0.2*inch))
            
            # Financial Summary
            content.append(Paragraph("Financial Summary", self.heading_style))
            total_income = float(summary_data[0])
            total_expense = float(summary_data[1])
            balance = total_income - total_expense
            
            summary_data = [
                ["Total Income:", f"{self.currency_symbol}{total_income:.2f}"],
                ["Total Expenses:", f"{self.currency_symbol}{total_expense:.2f}"],
                ["Balance:", f"{self.currency_symbol}{balance:.2f}"]
            ]
            summary_table = Table(summary_data, colWidths=[1.5*inch, 4*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (1, 0), (1, 0), colors.lightgreen),
                ('BACKGROUND', (1, 1), (1, 1), colors.lightcoral),
                ('BACKGROUND', (1, 2), (1, 2), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(summary_table)
            content.append(Spacer(1, 0.2*inch))
            
            # Charts
            if category_data and len(category_data) > 0:
                # Create expense breakdown chart using matplotlib
                content.append(Paragraph("Expense Breakdown by Category", self.heading_style))
                
                # Create pie chart with matplotlib and save to buffer
                plt.figure(figsize=(6, 4))
                labels = [item[0] for item in category_data]
                sizes = [float(item[1]) for item in category_data]
                chart_colors = [item[2] for item in category_data]  # Fixed: renamed to chart_colors
                
                plt.pie(sizes, labels=labels, colors=chart_colors, autopct='%1.1f%%', startangle=90)
                plt.axis('equal')
                plt.title('Expense Breakdown by Category')
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png')
                img_buffer.seek(0)
                
                # Add the image to the PDF
                img = Image(img_buffer, width=6*inch, height=4*inch)
                content.append(img)
                content.append(Spacer(1, 0.2*inch))
                plt.close()
            
            if monthly_data and len(monthly_data) > 0:
                # Create monthly trend chart
                content.append(Paragraph("Monthly Income and Expense Trend", self.heading_style))
                
                # Create line chart with matplotlib and save to buffer
                plt.figure(figsize=(7, 4))
                months = [item[0] for item in monthly_data]
                incomes = [float(item[1]) for item in monthly_data]
                expenses = [float(item[2]) for item in monthly_data]
                
                plt.plot(months, incomes, 'o-', color='green', label='Income')
                plt.plot(months, expenses, 'o-', color='red', label='Expenses')
                
                plt.title('Monthly Income and Expenses Trend')
                plt.xlabel('Month')
                plt.ylabel(f'Amount ({self.currency_symbol})')
                plt.xticks(rotation=45)
                plt.legend()
                plt.tight_layout()
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png')
                img_buffer.seek(0)
                
                # Add the image to the PDF
                img = Image(img_buffer, width=7*inch, height=4*inch)
                content.append(img)
                content.append(Spacer(1, 0.2*inch))
                plt.close()
            
            # Transaction History
            content.append(Paragraph("Transaction History", self.heading_style))
            
            if transactions:
                # Table header
                transaction_data = [["ID", "Date", "Type", "Category", "Amount", "Description"]]
                
                # Table data
                for transaction in transactions:
                    amount = f"{self.currency_symbol}{transaction[4]:.2f}"
                    transaction_data.append([
                        str(transaction[0]),
                        transaction[1].strftime('%Y-%m-%d'),
                        transaction[2],
                        transaction[3],
                        amount,
                        transaction[5]
                    ])
                
                # Create table
                transaction_table = Table(
                    transaction_data, 
                    colWidths=[0.5*inch, 1*inch, 0.8*inch, 1*inch, 0.8*inch, 2.4*inch]
                )
                
                # Style the table
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                    ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ])
                
                # Add alternating row colors
                for i in range(1, len(transaction_data)):
                    if i % 2 == 0:
                        table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
                
                transaction_table.setStyle(table_style)
                content.append(transaction_table)
            else:
                content.append(Paragraph("No transactions found.", self.normal_style))
            
            # Build the PDF
            doc.build(content)
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False