# Feedback Loop

This project has a narrow feedback loop:

```text
Real private migration
  -> generic public abstraction
  -> community review
  -> public kit iteration
  -> selected improvements back to the private setup
```

The public kit should only contain generic ideas, contracts, schemas, and examples.

The private setup may adopt useful public feedback, such as:

- clearer action names
- stricter action validation
- better shadow log fields
- simpler rollback checks
- improved troubleshooting steps

Private details should not be copied into the public kit.

