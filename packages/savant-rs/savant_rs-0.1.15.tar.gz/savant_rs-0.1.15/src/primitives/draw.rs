use pyo3::prelude::*;

#[pyclass]
#[derive(Clone, Copy, Debug)]
pub struct PaddingDraw {
    pub left: i64,
    pub top: i64,
    pub right: i64,
    pub bottom: i64,
}

#[pymethods]
impl PaddingDraw {
    #[classattr]
    const __hash__: Option<Py<PyAny>> = None;

    fn __repr__(&self) -> String {
        format!("{self:?}")
    }

    fn __str__(&self) -> String {
        self.__repr__()
    }

    #[new]
    #[pyo3(signature = (left=0, top=0, right=0, bottom=0))]
    pub fn new(left: i64, top: i64, right: i64, bottom: i64) -> Self {
        assert!(left >= 0);
        assert!(top >= 0);
        assert!(right >= 0);
        assert!(bottom >= 0);

        Self {
            left,
            top,
            right,
            bottom,
        }
    }

    #[getter]
    pub fn padding(&self) -> (i64, i64, i64, i64) {
        (self.left, self.top, self.right, self.bottom)
    }

    #[getter]
    pub fn left(&self) -> i64 {
        self.left
    }

    #[getter]
    pub fn top(&self) -> i64 {
        self.top
    }

    #[getter]
    pub fn right(&self) -> i64 {
        self.right
    }

    #[getter]
    pub fn bottom(&self) -> i64 {
        self.bottom
    }
}

#[pyclass]
#[derive(Clone, Copy, Debug)]
pub struct ColorDraw {
    pub red: i64,
    pub green: i64,
    pub blue: i64,
    pub alpha: i64,
}

#[pymethods]
impl ColorDraw {
    #[classattr]
    const __hash__: Option<Py<PyAny>> = None;

    fn __repr__(&self) -> String {
        format!("{self:?}")
    }

    fn __str__(&self) -> String {
        self.__repr__()
    }

    #[new]
    #[pyo3(signature = (red=0, green=255, blue=0, alpha=255))]
    pub fn new(red: i64, green: i64, blue: i64, alpha: i64) -> Self {
        assert!((0..=255).contains(&red));
        assert!((0..=255).contains(&green));
        assert!((0..=255).contains(&blue));
        assert!((0..=255).contains(&alpha));

        Self {
            red,
            green,
            blue,
            alpha,
        }
    }

    #[getter]
    pub fn bgra(&self) -> (i64, i64, i64, i64) {
        (self.blue, self.green, self.red, self.alpha)
    }

    #[getter]
    pub fn red(&self) -> i64 {
        self.red
    }

    #[getter]
    pub fn green(&self) -> i64 {
        self.green
    }

    #[getter]
    pub fn blue(&self) -> i64 {
        self.blue
    }

    #[getter]
    pub fn alpha(&self) -> i64 {
        self.alpha
    }
}

#[pyclass]
#[derive(Clone, Copy, Debug)]
pub struct BoundingBoxDraw {
    pub color: ColorDraw,
    pub thickness: i64,
    pub padding: Option<PaddingDraw>,
}

#[pymethods]
impl BoundingBoxDraw {
    #[classattr]
    const __hash__: Option<Py<PyAny>> = None;

    fn __repr__(&self) -> String {
        format!("{self:?}")
    }

    fn __str__(&self) -> String {
        self.__repr__()
    }

    #[new]
    #[pyo3(signature = (color, thickness = 1, padding = None))]
    pub fn new(color: ColorDraw, thickness: i64, padding: Option<PaddingDraw>) -> Self {
        assert!((0..=100).contains(&thickness));

        Self {
            color,
            thickness,
            padding,
        }
    }

    #[getter]
    pub fn color(&self) -> ColorDraw {
        self.color
    }

    #[getter]
    pub fn thickness(&self) -> i64 {
        self.thickness
    }

    #[getter]
    pub fn padding(&self) -> Option<PaddingDraw> {
        self.padding
    }
}

#[pyclass]
#[derive(Clone, Copy, Debug)]
pub struct DotDraw {
    pub color: ColorDraw,
    pub radius: i64,
}

#[pymethods]
impl DotDraw {
    #[classattr]
    const __hash__: Option<Py<PyAny>> = None;

    fn __repr__(&self) -> String {
        format!("{self:?}")
    }

    fn __str__(&self) -> String {
        self.__repr__()
    }

    #[new]
    #[pyo3(signature = (color, radius = 2))]
    pub fn new(color: ColorDraw, radius: i64) -> Self {
        assert!((0..=100).contains(&radius));

        Self { color, radius }
    }

    #[getter]
    pub fn color(&self) -> ColorDraw {
        self.color
    }

    #[getter]
    pub fn radius(&self) -> i64 {
        self.radius
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct LabelDraw {
    pub color: ColorDraw,
    pub font_scale: f64,
    pub thickness: i64,
    pub format: Vec<String>,
}

#[pymethods]
impl LabelDraw {
    #[classattr]
    const __hash__: Option<Py<PyAny>> = None;

    fn __repr__(&self) -> String {
        format!("{self:?}")
    }

    fn __str__(&self) -> String {
        self.__repr__()
    }

    #[new]
    #[pyo3(signature = (color, font_scale = 1.0, thickness = 1, format = vec!["{label}".to_string()]))]
    pub fn new(color: ColorDraw, font_scale: f64, thickness: i64, format: Vec<String>) -> Self {
        assert!((0.0..=200.0).contains(&font_scale));
        assert!((0..=100).contains(&thickness));

        Self {
            color,
            font_scale,
            thickness,
            format,
        }
    }

    #[getter]
    pub fn color(&self) -> ColorDraw {
        self.color
    }

    #[getter]
    pub fn font_scale(&self) -> f64 {
        self.font_scale
    }

    #[getter]
    pub fn thickness(&self) -> i64 {
        self.thickness
    }

    #[getter]
    pub fn format(&self) -> Vec<String> {
        self.format.clone()
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct ObjectDraw {
    pub bounding_box: Option<BoundingBoxDraw>,
    pub central_dot: Option<DotDraw>,
    pub label: Option<LabelDraw>,
    pub blur: bool,
}

#[pymethods]
impl ObjectDraw {
    #[classattr]
    const __hash__: Option<Py<PyAny>> = None;

    fn __repr__(&self) -> String {
        format!("{self:#?}")
    }

    fn __str__(&self) -> String {
        self.__repr__()
    }

    #[new]
    #[pyo3(signature = (bounding_box = None, central_dot = None, label = None, blur = false))]
    pub fn new(
        bounding_box: Option<BoundingBoxDraw>,
        central_dot: Option<DotDraw>,
        label: Option<LabelDraw>,
        blur: bool,
    ) -> Self {
        Self {
            bounding_box,
            central_dot,
            label,
            blur,
        }
    }

    #[getter]
    pub fn blur(&self) -> bool {
        self.blur
    }

    #[getter]
    pub fn bounding_box(&self) -> Option<BoundingBoxDraw> {
        self.bounding_box
    }

    #[getter]
    pub fn central_dot(&self) -> Option<DotDraw> {
        self.central_dot
    }

    #[getter]
    pub fn label(&self) -> Option<LabelDraw> {
        self.label.clone()
    }
}

#[derive(Clone, Debug)]
pub enum SetDrawLabelKind {
    OwnLabel(String),
    ParentLabel(String),
}

#[pyclass]
#[derive(Clone, Debug)]
#[pyo3(name = "SetDrawLabelKind")]
pub struct SetDrawLabelKindWrapper {
    pub(crate) inner: SetDrawLabelKind,
}

#[pymethods]
impl SetDrawLabelKindWrapper {
    #[classattr]
    const __hash__: Option<Py<PyAny>> = None;

    #[staticmethod]
    pub fn own(label: String) -> Self {
        Self {
            inner: SetDrawLabelKind::OwnLabel(label),
        }
    }

    #[staticmethod]
    pub fn parent(label: String) -> Self {
        Self {
            inner: SetDrawLabelKind::ParentLabel(label),
        }
    }

    pub fn is_own_label(&self) -> bool {
        matches!(self.inner, SetDrawLabelKind::OwnLabel(_))
    }

    pub fn is_parent_label(&self) -> bool {
        matches!(self.inner, SetDrawLabelKind::ParentLabel(_))
    }

    pub fn get_label(&self) -> String {
        match &self.inner {
            SetDrawLabelKind::OwnLabel(label) | SetDrawLabelKind::ParentLabel(label) => {
                label.clone()
            }
        }
    }
}
