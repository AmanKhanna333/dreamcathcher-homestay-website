# Dreamcatcher Homestay — Dharamkot, Dharamshala

A full-stack, hand-illustrated website for a real Himalayan homestay, built entirely on serverless AWS infrastructure.

## 🌐 Live Site
https://d1rb4b1kht3zmz.cloudfront.net/

## Design
Earthy, artistic, hand-drawn — every icon and illustration on the site is custom ink-line artwork (no stock photos or emoji), built in a consistent gold linework style. Features an animated aurora sky, shimmering gold accents, a gestural one-line wanderer figure, and organic painted-canvas frames instead of plain rectangles.

## Features
- Full booking system — guest fills a form, booking is saved and both guest and host receive email confirmation
- Interactive embedded Google Map for directions
- Auto-rotating testimonial carousel
- Click-to-expand gallery lightbox
- FAQ accordion
- Custom animated cursor, scroll progress bar, 3D tilt cards
- Fully responsive

## Architecture
Browser → CloudFront (HTTPS) → S3 (static site)
Booking Form → API Gateway → Lambda → DynamoDB + SES


| Service | Role |
|---|---|
| Amazon S3 | Hosts the static website |
| Amazon CloudFront | HTTPS delivery + global CDN |
| Amazon API Gateway | POST /booking endpoint |
| AWS Lambda (Python) | Processes bookings, saves to DB, sends emails |
| Amazon DynamoDB | Stores every booking inquiry |
| Amazon SES | Sends guest confirmation + host alert emails |

## Status
Live and fully functional. SES is currently in sandbox mode — production access requested to enable guest confirmation emails to any address (currently host email always works; guest confirmation works for verified addresses only, guests are still notified via WhatsApp in the meantime).

Photo placeholders are intentional custom illustrations — real property photography to be added in the next iteration.

## Contact
WhatsApp: +91 97368 92850
Instagram: [@dreamcatcher_homestays](https://instagram.com/dreamcatcher_homestays) · [@dreamcatcher.dharamkot](https://instagram.com/dreamcatcher.dharamkot)
