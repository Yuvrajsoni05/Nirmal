document.addEventListener('DOMContentLoaded', function () {
    const JobInput = document.getElementById('job_date');
    const JobError = document.getElementById('job_date_error');

    const BillInput = document.getElementById('bill_no');
    const BillError = document.getElementById('bill_no_error');

    const CompanyInput = document.getElementById('company_name');
    const CompanyError = document.getElementById('company_name_error');

    const Job_Name_Input = document.getElementById('job_name');
    const Job_Name_Error = document.getElementById('job_name_error');

    const Job_Type_Input = document.getElementById('job_type');
    const Job_Type_Error = document.getElementById('job_type_error');

    const NOC_Input = document.getElementById('noc');
    const NOC_Error = document.getElementById('noc_error');

    const prpc_purchase_Input = document.getElementById('prpc_purchase');
    const prpc_purchase_Error = document.getElementById('prpc_purchase_error');

    const prpc_sell_Input = document.getElementById('prpc_sell');
    const prpc_sell_Error = document.getElementById('prpc_sell_error');

    const cylinder_diameter_Input = document.getElementById('cylinder_diameter');
    const cylinder_diameter_Error = document.getElementById('cylinder_diameter_error');
    const cylinder_height_Input = document.getElementById('cylinder_height');
    const cylinder_height_Error = document.getElementById('cylinder_height_error');



    const pouch_diameter_Input = document.getElementById('pouch_diameter');
    const pouch_diameter_Error = document.getElementById('pouch_diameter_error');
    const pouch_height_Input = document.getElementById('pouch_height');
    const pouch_height_Error = document.getElementById('pouch_height_error');



    const pouch_open_diameter_Input = document.getElementById('pouch_open_diameter');
    const pouch_open_diameter_Error = document.getElementById('pouch_open_diameter_error');
    const pouch_open_height_Input = document.getElementById('pouch_open_height');
    const pouch_open_height_Error = document.getElementById('pouch_open_height_error');


    const cylinder_made_in_Input = document.getElementById('cylinder_made_in');
    const cylinder_made_in_Error = document.getElementById('cylinder_made_in_error');

    const pouch_combination1_Input = document.getElementById('pouch_combination1');
    const pouch_combination1_Error = document.getElementById('pouch_combination1_error');
    const pouch_combination2_Input = document.getElementById('pouch_combination2');
    const pouch_combination2_Error = document.getElementById('pouch_combination2_error');

    const myForm = document.getElementById('job_detail_form');



    function validateCylinderMade() {
        if (cylinder_made_in_Input.value.trim() === '') {
            cylinder_made_in_Error.style.display = 'block';
            return false;
        } else {
            cylinder_made_in_Error.style.display = 'none';
            return true;
        }
    }


    
    function validateJob() {
        if (JobInput.value.trim() === '') {
            JobError.style.display = 'block';
            return false;
        } else {
            JobError.style.display = 'none';
            return true;
        }
    }

    function validateBill() {
        if (BillInput.value.trim() === '') {
            BillError.style.display = 'block';
            return false;
        } else {
            BillError.style.display = 'none';
            return true;
        }
    }

    function validateCompany() {
        if (CompanyInput.value.trim() === '') {
            CompanyError.style.display = 'block';
            return false;
        } else {
            CompanyError.style.display = 'none';
            return true;
        }
    }

    function validateJobName() {
        if (Job_Name_Input.value.trim() === '') {
            Job_Name_Error.style.display = 'block';
            return false;
        } else {
            Job_Name_Error.style.display = 'none';
            return true;
        }
    }

    function validateJobType() {
        if (Job_Type_Input.value.trim() === '') {
            Job_Type_Error.style.display = 'block';
            return false;
        } else {
            Job_Type_Error.style.display = 'none';
            return true;
        }
    }

    function validateNOC() {
        if (NOC_Input.value.trim() === '') {
            NOC_Error.style.display = 'block';
            return false;
        } else {
            NOC_Error.style.display = 'none';
            return true;
        }
    }

    function validatePrpcPurchase() {
        if (prpc_purchase_Input.value.trim() === '') {
            prpc_purchase_Error.style.display = 'block';
            return false;
        } else {
            prpc_purchase_Error.style.display = 'none';
            return true;
        }
    }

    function validatePrpcSell() {
        if (prpc_sell_Input.value.trim() === '') {
            prpc_sell_Error.style.display = 'block';
            return false;
        } else {
            prpc_sell_Error.style.display = 'none';
            return true;
        }
    }

    function validateCylinderDiameter() {
        if (cylinder_diameter_Input.value.trim() === '') {
            cylinder_diameter_Error.style.display = 'block';
            return false;
        } else {
            cylinder_diameter_Error.style.display = 'none';
            return true;
        }
    }

    function validateCylinderHeight() {
        if (cylinder_height_Input.value.trim() === '') {
            cylinder_height_Error.style.display = 'block';
            return false;
        } else {
            cylinder_height_Error.style.display = 'none';
            return true;
        }
    }




    function validatePouchOpenDiameter() {
        if (pouch_open_diameter_Input.value.trim() === '') {
            pouch_open_diameter_Error.style.display = 'block';
            return false;
        } else {
            pouch_open_diameter_Error.style.display = 'none';
            return true;
        }
    }

    function validatePouchOpenHeight() {
        if (pouch_open_height_Input.value.trim() === '') {
            pouch_open_height_Error.style.display = 'block';
            return false;
        } else {
            pouch_open_height_Error.style.display = 'none';
            return true;
        }
    }



    function validatePouchDiameter() {
        if (pouch_diameter_Input.value.trim() === '') {
            pouch_diameter_Error.style.display = 'block';
            return false;
        } else {
            pouch_diameter_Error.style.display = 'none';
            return true;
        }
    }

    function validatePouchHeight() {
        if (pouch_height_Input.value.trim() === '') {
            pouch_height_Error.style.display = 'block';
            return false;
        } else {
            pouch_height_Error.style.display = 'none';
            return true;
        }
    }




    function validatePouchCombination1() {
        if (pouch_combination1_Input.value.trim() === '') {
            pouch_combination1_Error.style.display = 'block';
            return false;
        } else {
            pouch_combination1_Error.style.display = 'none';
            return true;
        }
    }

    function validatePouchCombination2() {
        if (pouch_combination2_Input.value.trim() === '') {
            pouch_combination2_Error.style.display = 'block';
            return false;
        } else {
            pouch_combination2_Error.style.display = 'none';
            return true;
        }
    }

    
  
    function validateForm() {
        const isJobValid = validateJob();
        const isBillValid = validateBill();
        const isCompanyValid = validateCompany();
        const isJobNameValid = validateJobName();
        const isJobTypeValid = validateJobType();
        const isNOCValid = validateNOC();
        const isPrpcPurchaseValid = validatePrpcPurchase();
        const isPrpcSellValid = validatePrpcSell();
        const isCylinderDiameterValid = validateCylinderDiameter();
        const isCylinderHeightValid = validateCylinderHeight();
        const isCylinderMadeIn = validateCylinderMade();
        const isPouchDiameterValid = validatePouchDiameter();
        const isPouchrHeightValid = validatePouchHeight();
        const isPouchOpenDiameterValid = validatePouchOpenDiameter();
        const isPouchOpenHeightValid = validatePouchOpenHeight(); 
        const isPouchCombination1 = validatePouchCombination1();
        const isPouchCombination2 = validatePouchCombination2(); 
        return (
            isJobValid &&
            isBillValid &&
            isCompanyValid &&
            isJobNameValid &&
            isJobTypeValid &&
            isNOCValid &&
            isPrpcPurchaseValid &&
            isPrpcSellValid &&
            isCylinderDiameterValid &&
            isCylinderHeightValid &&
            isCylinderMadeIn && 
            isPouchDiameterValid &&
            isPouchrHeightValid &&
            isPouchOpenDiameterValid &&
            isPouchOpenHeightValid &&
            isPouchCombination1 &&
            isPouchCombination2 

        );
    }


    JobInput.addEventListener('input', validateJob);
    JobInput.addEventListener('blur', validateJob);

    BillInput.addEventListener('input', validateBill);
    BillInput.addEventListener('blur', validateBill);

    CompanyInput.addEventListener('input', validateCompany);
    CompanyInput.addEventListener('blur', validateCompany);

    Job_Name_Input.addEventListener('input', validateJobName);
    Job_Name_Input.addEventListener('blur', validateJobName);

    Job_Type_Input.addEventListener('input', validateJobType);
    Job_Type_Input.addEventListener('blur', validateJobType);

    NOC_Input.addEventListener('input', validateNOC);
    NOC_Input.addEventListener('blur', validateNOC);

    prpc_purchase_Input.addEventListener('input', validatePrpcPurchase);
    prpc_purchase_Input.addEventListener('blur', validatePrpcPurchase);

    prpc_sell_Input.addEventListener('input', validatePrpcSell);
    prpc_sell_Input.addEventListener('blur', validatePrpcSell);

    cylinder_diameter_Input.addEventListener('input', validateCylinderDiameter);
    cylinder_diameter_Input.addEventListener('blur', validateCylinderDiameter);

    cylinder_height_Input.addEventListener('input', validateCylinderHeight);
    cylinder_height_Input.addEventListener('blur', validateCylinderHeight);

    cylinder_made_in_Input.addEventListener('input',validateCylinderMade);
    cylinder_made_in_Input.addEventListener('blur', validateCylinderMade);


    pouch_diameter_Input.addEventListener('input', validatePouchDiameter);
    pouch_diameter_Input.addEventListener('blur', validatePouchDiameter);

    pouch_height_Input.addEventListener('input',validatePouchHeight);
    pouch_height_Input.addEventListener('blur', validatePouchHeight);

    pouch_open_diameter_Input.addEventListener('input', validatePouchOpenDiameter);
    pouch_open_diameter_Input.addEventListener('blur', validatePouchOpenDiameter);

    pouch_open_height_Input.addEventListener('input',validatePouchOpenHeight);
    pouch_open_height_Input.addEventListener('blur', validatePouchOpenHeight);


    pouch_combination1_Input.addEventListener('input', validatePouchCombination1);
    pouch_combination1_Input.addEventListener('blur',validatePouchCombination1);

    pouch_combination2_Input.addEventListener('input',validatePouchCombination2);
    pouch_combination2_Input.addEventListener('blur', validatePouchCombination2);



    myForm.addEventListener('submit', function (event) {
        event.preventDefault();

        if (validateForm()) {
    
            myForm.submit();
        } else {
        
            const firstError = document.querySelector('[style*="display: block"]');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});