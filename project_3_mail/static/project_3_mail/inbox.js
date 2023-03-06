document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(emailid = undefined) {

  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  //Collect the compostion fields
  let recipient = document.querySelector('#compose-recipients');
  let subject = document.querySelector('#compose-subject');
  let body = document.querySelector('#compose-body');

  // Clear out composition fields
  recipient.value = ''
  subject.value = ''
  body.value = ''

  // If an emailid was provided, fetch this email in order to reply
  if (parseInt(emailid)) {
    fetch(`/mail/emails/${emailid}`)
      .then(response => {
        return response.json()
      })
      .then(email => {
        // we need to send to the original sender not this reciver
        email.recipients[email.recipients.indexOf(document.querySelector('#user-email').value)] = email.sender

        //prefil values into the form
        recipient.value = email.recipients.join(', ')
        subject.value = email.subject.substring(0, 3) == 'RE:' ? email.subject : `RE: ${email.subject}`
        body.value = `\n
On ${email.timestamp} ${email.sender} wrote:
${email.body}
      `
      });
  }

  // make a post request to send the email
  document.querySelector('#compose-submit').addEventListener('click', (e) => {
    e.stopImmediatePropagation()
    fetch('/mail/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
      .then(response => response.json())
      .then(result => {
        // If theres an error we alert the user to this and let them resubmit else load inbox
        if (result.error) {
          alert(result.error)
        } else {
          load_mailbox('inbox')
        }
      });
  })
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch all emails belonging to the appropriate user and mailbox
  fetch(`/mail/emails/${mailbox}`)
    .then(response => {
      return response.json()
    })
    .then(emails => {
      // For every email we add it to the mailbox in a simple 3 column layout
      for (e in emails) {
        email = emails[e]
        document.querySelector('#emails-view').innerHTML +=
          `<div class="row email ${email.read && mailbox != 'sent' ? 'read' : ''}" onclick="view_email(${email.id})">
          <div class="col-6">${email.subject} </div>
          <div class="col-3">${mailbox != 'sent' ? `From ${email.sender}` : `To ${email.recipients.join(', ')}`} </div>
          <div class="col-3">at ${email.timestamp} </div>
        </div>`

      }
    });
}


function view_email(id) {

  // Show the email and hide all other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Fetch the email to view
  fetch(`/mail/emails/${id}`)
    .then(response => {
      return response.json()
    })
    .then(email => {
      // Check if there was any errors loading file and notice to the error
      if (email.error) {
        document.querySelector('#email-view').innerHTML = `<h2><strong>Error:</strong> ${email.error}</h2>`
      } else {
        // If email has not previously be read we now mark it as read
        if (!email.read) {
          fetch(`/mail/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          })
        }

        // Load the email content
        document.querySelector('#email-view').innerHTML = `
        <div class="row">
          <div class="col-9"><h2>${email.subject}</h2></div>
          <div class="col-3">
            ${email.user == email.sender ? `` : `<button class="btn btn-outline-dark email-btn" onclick="archive(${id},${!email.archived})">${email.archived ? 'Un Archive' : 'Archive'}</button>`}
            <button class="btn btn-outline-info email-btn" onclick="compose_email(${email.id})">Reply</button>
          </div>
        </div>
        <div><strong>To:</strong> ${email.recipients.join(', ')}</div>
        <div><strong>From:</strong> ${email.sender}</div>
        <div><strong>Recieved at:</strong> ${email.timestamp}</div>
        <hr>
        <div><p>${email.body.replace(/\n/g, "<br />")}</p></div>
        `
      }
    });
}

function archive(id, state) {
  fetch(`/mail/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: state
    })
  }).then(response => {
    load_mailbox('inbox')
  })
}