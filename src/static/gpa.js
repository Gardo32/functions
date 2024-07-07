function addSubjectField() {
    var numSubjects = parseInt(document.getElementById('num_subjects').value);
    var subjectTableBody = document.getElementById('subjectTableBody');
    var subjectIndex = subjectTableBody.children.length + 1;

    var newRow = `
        <tr id="subjectRow_${subjectIndex}">
            <td>Subject ${subjectIndex}</td>
            <td><input type="number" id="marks_${subjectIndex}" name="marks_${subjectIndex}" class="form-control" required></td>
            <td><input type="number" id="hours_${subjectIndex}" name="hours_${subjectIndex}" class="form-control" required></td>
        </tr>
    `;
    
    subjectTableBody.insertAdjacentHTML('beforeend', newRow);

    // Add event listener to restrict marks input to maximum 100
    var marksInput = document.getElementById(`marks_${subjectIndex}`);
    marksInput.addEventListener('change', function() {
        if (parseInt(this.value) > 100) {
            this.value = 100;
        }
    });
}

function removeSubjectField() {
    var subjectTableBody = document.getElementById('subjectTableBody');
    if (subjectTableBody.children.length > 0) {
        subjectTableBody.removeChild(subjectTableBody.lastElementChild);
    }
}

// Update subject fields based on num_subjects input
document.getElementById('num_subjects').addEventListener('change', function() {
    var numSubjects = parseInt(this.value);
    var subjectTableBody = document.getElementById('subjectTableBody');
    var currentSubjects = subjectTableBody.children.length;
    
    if (numSubjects > currentSubjects) {
        for (var i = currentSubjects + 1; i <= numSubjects; i++) {
            var newRow = `
                <tr id="subjectRow_${i}">
                    <td>Subject ${i}</td>
                    <td><input type="number" id="marks_${i}" name="marks_${i}" class="form-control" required></td>
                    <td><input type="number" id="hours_${i}" name="hours_${i}" class="form-control" required></td>
                </tr>
            `;
            subjectTableBody.insertAdjacentHTML('beforeend', newRow);

            // Add event listener to restrict marks input to maximum 100
            var marksInput = document.getElementById(`marks_${i}`);
            marksInput.addEventListener('change', function() {
                if (parseInt(this.value) > 100) {
                    this.value = 100;
                }
            });
        }
    } else if (numSubjects < currentSubjects) {
        for (var i = currentSubjects; i > numSubjects; i--) {
            var subjectRow = document.getElementById(`subjectRow_${i}`);
            if (subjectRow) {
                subjectRow.parentNode.removeChild(subjectRow);
            }
        }
    }
});
