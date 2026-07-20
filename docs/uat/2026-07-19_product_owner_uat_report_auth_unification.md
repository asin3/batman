# PRODUCT OWNER UAT Report

Date: 20 Jul 2026
Time: 14:40 IST
Tester: Amit
Repository: local
Branch: CPS-001-impl-auth-unification
CPS: CPS-001-impl-auth-unification
Sprint Workspace: CPS001_AUTH_20260720-2115

---

# UAT Report 

1. Environment Sanity

PASS


3. Test Execution Log

For every test record:

- Test Number
- Test Name
- Expected Result
- Actual Result
- Status
- Observation

Test Number A. 
Test Name: virtual env switch
Actual Result: enev worked after i doing - 
        # 3. Activate it 
          source .venv/bin/activate 
Status: Pass


Test Number: B.
Test Name: Batman-core login 
Actual Result: successful, able to execute a question, so I say Login 
                ### Drona (with authentication)
                bash
                streamlit run src/ui/app.pyfor 
Status: PASS 
Evidence: TEST-b_PASS.png

Test Number: C. 
Test Name: Batman-dd login
Actual Result: screen displayed, then again popup, that login doesn't do anything.. I guess this was expected for DD..i understand unification will happen in phase 2? correct me if i am wrong..Not sure about expeted result..
   '### Batman DD (for "My Plan & Progress" link validation)'
    bash streamlit run src/batman_dd/app.py 
Status: FAIL
Evidence: TEST-C_FAIL.png


### Obeservation -
 1.Another thing Orion said test data as amit.sinha@gmail.com, which was correct when were testing Drona with STD001, because that's not real gmailID.. Now I am testing with real emailID(amit.sinha4@gmail.com) and able to login core successfully after Orion's change..So advice in this situation