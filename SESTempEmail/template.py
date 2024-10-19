# Define the template
template_name = 'MyContractTemplate'
template_contract = {
    'TemplateName': template_name,  # Name for your template
    'SubjectPart': 'Create new contract',
    'TextPart': 'Dear {{name}},\n\nYou have a new contract assigned.\n\nBest,\nTeam',
    'HtmlPart': '''
        <html>
        <body>
            <h1>Hello {{name}},</h1>
            <p>You have a new contract assigned.</p>
            <p>Best Regards,<br>Team</p>
        </body>
        </html>
    '''
}